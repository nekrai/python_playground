import unittest
import alert_me


class TestAlert(unittest.TestCase):

    def tearDown(self):
        print self.lol

    def mock_print(self, message):
        self.was_called = True
        self.with_message = message

        if self.test_case == 1:
            self.lol = 'potatoes'
        elif self.test_case == 2:
            self.lol = 'fiambre'

    def test_alert_default(self):
        self.test_case = 1
        alert_me.print_message = self.mock_print
        alert_me.alert()
        self.assertTrue(self.was_called)
        self.assertEqual('alert!', self.with_message)

    def test_alert_with_message(self):
        self.test_case = 2
        alert_me.print_message = self.mock_print
        alert_me.alert('bla')
        self.assertTrue(self.was_called)
        self.assertEqual('bla', self.with_message)



if __name__ == '__main__':
    unittest.main()