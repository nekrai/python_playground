import unittest
import alert_me


class TestAlert(unittest.TestCase):

    def mock_print(self, message):
        self.was_called = True
        self.with_message = message

    def test_alert_default(self):
        alert_me.print_message = self.mock_print
        alert_me.alert()
        self.assertTrue(self.was_called)
        self.assertEqual('alert!', self.with_message)

    def test_alert_with_message(self):
        alert_me.print_message = self.mock_print
        alert_me.alert('bla')
        self.assertTrue(self.was_called)
        self.assertEqual(self.with_message, 'bla')

if __name__ == '__main__':
    unittest.main()