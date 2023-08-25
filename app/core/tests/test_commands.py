"""
Test custom Django management commands.
"""

from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# Mocking the 'check' method provided by the 'BaseCommand' class inside of wait_for_db.py
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    # Test commands
    # pass in the mocked 'check' method as an argument
    def test_wait_for_db_ready(self, patched_check):
        # Test waiting for database if database ready
        # when the mocked 'check' method is executed, do nothing other than return True
        # Setup inpput
        patched_check.return_value = True

        # actually execute the code in wait_for_db.py, check if the 'Command' class exists
        # execute code to be tested
        call_command('wait_for_db')

        # actually calls the mocked 'check' method with the default database
        # assertion (check output)
        patched_check.assert_called_once_with(databases=['default'])

    # mocks the sleep function
    @patch('time.sleep')
    # add your arguments from the inside-out, i.e patched_sleep before patched_check
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        # Test waiting for database when getting OperationalError
        # Raise exceptions
        # The '* 2' here means the first 2 times we call the mocked 'check' method, it should raise the Psycopg2Error
        # The '* 3' here means after the first 2 times we called the mocked 'check' method, it should raise the OperationalError 3 times
        # The 6th time we call the mocked 'check' method, return True
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)

        patched_check.assert_called_with(databases=['default'])
