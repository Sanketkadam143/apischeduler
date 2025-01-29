import unittest
import logging
from datetime import datetime, time as dt_time, timedelta
from unittest.mock import MagicMock, patch
from utils import timeparser, set_logger, make_api_call
from main import main


class TestMainFunction(unittest.TestCase):
    @patch('utils.timeparser')
    @patch('main.schedule_api_call')
    def test_main(self, mock_parse, mock_schedule):
        mock_parse.side_effect = [dt_time(10, 0, 0), dt_time(11, 0, 0)]
        mock_schedule.return_value = MagicMock()

        with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(timestamps="10:00:00,11:00:00")):
            main()
        self.assertEqual(mock_parse.call_count, 2)
        self.assertEqual(mock_schedule.call_count, 2)


if __name__ == '__main__':
    unittest.main()