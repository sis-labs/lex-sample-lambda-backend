import unittest
import os
import sys
from pathlib import Path
import json
import logging
import datetime

import lambda_function as lf

logger = logging.getLogger()
logger.level = logging.DEBUG

class TestDispatch(unittest.TestCase):

    def setUp(self):
        self.stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(self.stream_handler)

    def tearDown(self):
        logger.removeHandler(self.stream_handler)
        self.stream_handler = None

    def fetch_event_by_name(self, filename):
        """Helper function to load event
        :param filename: the name of the file to laod
        :returns: object
        """
        dirname = os.path.dirname(os.path.realpath(__file__))
        evt = Path('{}/../samples/{}'.format(dirname, filename)).read_text()
        return json.loads(evt)

    def fetch_event(self):
        filename = 'event.json'
        return self.fetch_event_by_name(filename)

    def get_future_date(self, days=1):
        now = datetime.datetime.now()
        return now + datetime.timedelta(days=days)

    def test_load_event(self):
        # GIVEN
        evt = self.fetch_event()

        # THEN
        self.assertNotEqual(None, evt)

    def test_dispatch_success(self):
        # GIVEN
        evt = self.fetch_event()
        
        # WHEN
        r = lf.lambda_handler(evt, {})

        # THEN
        self.assertNotEqual(None, r)

    def test_dispatch_wrong_appointment(self):
        # GIVEN
        evt = self.fetch_event()
        evt['currentIntent']['name'] = 'WrongName'

        # WHEN / THEN
        with self.assertRaises(Exception):
            lf.lambda_handler(evt, {})

    def test_get_availabilities(self):
        # GIVEN
        date = self.get_future_date()

        # WHEN
        availabilities = lf.get_availabilities(date.isoformat())

        # THEN
        if date.weekday() in [0,2,4]:
            self.assertNotEqual([], availabilities)
        if date.weekday() not in [0,2,4]:
            self.assertEqual([], availabilities)
