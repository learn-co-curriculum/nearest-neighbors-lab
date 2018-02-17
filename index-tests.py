import unittest
from ipynb.fs.full.index import trips

class TestDistance(unittest.TestCase):
    def test_parse_trips(self):
        self.assertEqual(parse_trips(trips), {'pickup_latitude': 40.64499, 'pickup_longitude': -73.78115, 'trip_distance': 18.38})
