import unittest
import alert_me
from mock import MagicMock


class TestAlert(unittest.TestCase):

    _mocked_values = {1: 'test1', 2: 'test2'}

    def mock_fetch_message(self, args):
        return self._mocked_values[args]

    def test_alert_default(self):
        # arrange
        alert_me.print_message = MagicMock()
        # act
        alert_me.alert(1)
        # assert
        alert_me.print_message.assert_called_once_with('green alert!')

    def test_alert_with_message(self):
        # arrange
        alert_me.print_message = MagicMock()
        alert_me.fetch_message = MagicMock(side_effect=self.mock_fetch_message)
        # act
        alert_me.alert(1)
        # assert
        alert_me.print_message.assert_called_once_with('test1')



if __name__ == '__main__':
    unittest.main()