import unittest
import sys
import warnings
from contextlib import contextmanager
from io import StringIO

sys.path.insert(0, '..')
from ProgressBar import ProgressBar


class ProgressBarTestCase(unittest.TestCase):
    def setUp(self):
        self.progressbar = ProgressBar(1000)

    def tearDown(self):
        self.progressbar = None

    @contextmanager
    def captured_output(self):
        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_out, old_err

    def reset_state(self):
        self.progressbar.total = 1000
        self.progressbar.current = 0
        self.progressbar.time_running = 0
        self.progressbar.bar = '[]'.format(' ' * 100)
        self.progressbar.percentage = 0
        self.progressbar.number_of_stripes = 0
        self.progressbar.number_of_spaces = 100

    def test_initial_state(self):
        self.assertEqual(self.progressbar.total, 1000, 'Total should be 1000')
        self.assertEqual(self.progressbar.current, 0, 'Current stage should be 0')
        self.assertEqual(self.progressbar.time_running, 0, 'Time running should be 0')
        self.assertEqual(self.progressbar.bar, '[]'.format(' ' * 100), 'Progressbar should be empty')
        self.assertEqual(self.progressbar.percentage, 0, 'Percentage should be 0')
        self.assertEqual(self.progressbar.number_of_stripes, 0, 'Number of stripes should be 0')
        self.assertEqual(self.progressbar.number_of_spaces, 100, 'Number of spaces should be 100')

    def test_get_next(self):
        self.progressbar.get_next(10)
        self.assertEqual(self.progressbar.current, 10, 'Current stage should be 10')
        self.assertEqual(self.progressbar.bar, '\r[-{}] 1%'.format(99*" "))
        self.reset_state()

    def test_get_next_zero_total(self):
        self.progressbar.total = 0
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.progressbar.get_next(10)
            self.assertTrue(issubclass(w[-1].category, UserWarning))
            print(str(w[-1].message))
            self.assertEqual(str(w[-1].message), "Total is zero, instantly done")
        self.reset_state()

    def test_get_percentage(self):
        self.progressbar.current = 100
        percentage = self.progressbar.get_percentage()
        self.assertEqual(percentage, 10, 'Percentage should be 10% (100/1000)')
        self.reset_state()

    def test_get_percentage_higher_than_total(self):
        self.progressbar.current = 1100
        percentage = self.progressbar.get_percentage()
        self.assertEqual(percentage, 100, 'Percentage should be 100% (never higher than 100)')
        self.reset_state()

    def test_print_progress(self):
        self.progressbar.current = 250
        self.progressbar.print_progress()
        self.assertEqual(self.progressbar.number_of_stripes, 25, '25 Stripes should be shown')
        self.assertEqual(self.progressbar.number_of_spaces, 75, '75 Spaces should be shown')
        self.reset_state()

    def test_get_done_message_without_input(self):
        self.progressbar.time_running = 1.123
        with warnings.catch_warnings(record=True) as warning_list:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            message = self.progressbar.get_done_message()
            self.assertEqual(len(warning_list), 0, 'There should be no warnings')
            self.assertEqual(message, '\nDone in 1.123 seconds')
        self.reset_state()

    def test_get_done_message_with_minutes(self):
        self.progressbar.time_running = 60
        with warnings.catch_warnings(record=True) as warning_list:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            message = self.progressbar.get_done_message('min')
            self.assertEqual(len(warning_list), 0, 'There should be no warnings')
            self.assertEqual(message, '\nDone in 1.0 minutes')
        self.reset_state()

    def test_get_done_message_with_hours(self):
        self.progressbar.time_running = 360
        with warnings.catch_warnings(record=True) as warning_list:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            message = self.progressbar.get_done_message('h')
            self.assertEqual(len(warning_list), 0, 'There should be no warnings')
            self.assertEqual(message, '\nDone in 0.1 hours')
        self.reset_state()

    def test_get_done_message_with_wrong_input(self):
        self.progressbar.time_running = 1.123
        with warnings.catch_warnings(record=True) as warning_list:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            message = self.progressbar.get_done_message('x')
            self.assertEqual(len(warning_list), 1, 'Length of warnings should be 1')
            self.assertTrue(issubclass(warning_list[-1].category, UserWarning), 'Warning class should be of catagory "Userwarning"')
            self.assertEqual(str(warning_list[-1].message),
                             'unsupported type: x instead of ["sec", "min", "h"], returning output in seconds',
                             'Message should be telling output is shown in seconds because type was not supported')
        self.reset_state()


def suite():
    tests = ['test_initial_state', 'test_get_next', 'test_get_next_zero_total', 'test_get_percentage',
             'test_get_percentage_higher_than_total','test_print_progress',
             'test_get_done_message', 'test_get_done_message_with_wrong_input']
    return unittest.TestSuite(map(ProgressBarTestCase, tests))


if __name__ == '__main__':
    suite()
