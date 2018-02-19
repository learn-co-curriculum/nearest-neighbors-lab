import unittest
from ipynb.fs.full.index import (trips, parse_trips, trip_latitudes,
    trip_longitudes, distance_location, nearest_neighbors, median_of)

class TestDistance(unittest.TestCase):
    parsed_trips = parse_trips(trips)

    def test_parse_trips_has_lat_and_longitude(self):
        self.assertEqual(parse_trips(trips)[0], {'pickup_latitude': 40.64499, 'pickup_longitude': -73.78115, 'trip_distance': 18.38}, 'Has latitudes and longitudes of the first trip')

    def test_parse_trips_returns_entry_for_each_trip(self):
        self.assertEqual(len(parse_trips(trips)), 1000, 'Returns entry for each trip')

    def test_parse_trips_returns_attributes_of_lat_long_and_distance(self):
        parsed_trips = parse_trips(trips)
        trip_attributes = set([key for trip in parsed_trips for key in list(trip.keys())])
        self.assertEqual(trip_attributes, {'pickup_latitude', 'pickup_longitude', 'trip_distance'}, 'Has attributes of lat, long, and distance')

    def test_trip_latitudes(self):
        trip_lats = trip_latitudes(TestDistance.parsed_trips)
        self.assertEqual(trip_lats[0], 40.64499, 'returns an array of trip latitudes')
        self.assertEqual(len(trip_lats), 1000, 'returns a latitude for every parsed trip')

    def test_trip_longitudes(self):
        trip_longs = trip_longitudes(TestDistance.parsed_trips)
        self.assertEqual(trip_longs[0], -73.78115, 'returns an array of trip longitudes')
        self.assertEqual(len(trip_longs), 1000, 'returns a longitude for every parsed trip')

    def test_distance_location(self):
        first_trip = TestDistance.parsed_trips[0]
        second_trip = TestDistance.parsed_trips[1]
        distance = distance_location(first_trip, second_trip)
        self.assertEqual(distance, 0.23505256047318146)

    def test_nearest_neighbors(self):
        first_trip = TestDistance.parsed_trips[0]
        neighbors = nearest_neighbors(first_trip, TestDistance.parsed_trips)
        self.assertEqual(len(neighbors), 3, 'it returns 3 neighbors by default')

    def test_nearest_neighbors_attributes(self):
        first_trip = TestDistance.parsed_trips[0]
        neighbors = nearest_neighbors(first_trip, TestDistance.parsed_trips)
        neighbors_attributes = set([key for neighbor in neighbors for key in list(neighbor.keys())])
        self.assertEqual(neighbors_attributes, {'distance', 'pickup_longitude', 'pickup_latitude', 'trip_distance'}, 'it includes a key of distance')

    def test_median_of(self):
        median_distance = median_of(TestDistance.parsed_trips)
        self.assertEqual(median_distance, 1.66, 'given a list of neighbors, it returns the median trip distance')
