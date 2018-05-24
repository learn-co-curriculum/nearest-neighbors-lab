import unittest
from ipynb.fs.full.index import (trips, parse_trips, distance_location, location, to_marker,
 markers_from_trips, map_from, add_markers, distance_location, distance_between_neighbors, distance_all, nearest_neighbors)
import json
class TestDistance(unittest.TestCase):
    parsed_trips = parse_trips(trips)

    def test_parse_trips_has_lat_and_longitude(self):
        first_trip = {'pickup_latitude': '40.64499',
        'pickup_longitude': '-73.781149999999997',
        'trip_distance': '18.379999999999999'}
        parsed_first = parse_trips(trips)[0]
        self.assertEqual(round(float(parsed_first['pickup_latitude']), 2), round(float(first_trip['pickup_latitude']), 2), 'Has latitude of the first trip')
        self.assertEqual(round(float(parsed_first['pickup_longitude']), 2), round(float(first_trip['pickup_longitude']), 2), 'Has longitude of the first trip')
        self.assertEqual(round(float(parsed_first['trip_distance']), 2), round(float(first_trip['trip_distance']), 2), 'Has trip distance of the first trip')

    def test_parse_trips_returns_entry_for_each_trip(self):
        self.assertEqual(len(parse_trips(trips)), 1000, 'Returns entry for each trip')

    def test_parse_trips_returns_attributes_of_lat_long_and_distance(self):
        parsed_trips = parse_trips(trips)
        trip_attributes = set([key for trip in parsed_trips for key in list(trip.keys())])
        self.assertEqual(trip_attributes, {'pickup_latitude', 'pickup_longitude', 'trip_distance'}, 'Has attributes of lat, long, and distance')

    def test_location(self):
        first_trip = {'pickup_latitude': 40.64499, 'pickup_longitude': -73.78115,  'trip_distance': 18.38}
        self.assertEqual(location(first_trip), [40.64499, -73.78115], 'Has attributes of lat, long, and distance')

    def test_to_marker(self):
        marker = to_marker([40.7589, -73.9851])
        self.assertEqual(marker.location, [40.7589, -73.9851])
        self.assertEqual(json.loads(marker.options)['radius'], 6)

    def test_markers_from_trips(self):
        cleaned_trips = [{'pickup_latitude': 40.64499, 'pickup_longitude': -73.78115, 'trip_distance': 18.38},
         {'pickup_latitude': 40.766931, 'pickup_longitude': -73.982098, 'trip_distance': 1.3},
         {'pickup_latitude': 40.77773, 'pickup_longitude': -73.951902, 'trip_distance': 4.5},
         {'pickup_latitude': 40.795678, 'pickup_longitude': -73.971049, 'trip_distance': 2.4}]
        trip_markers = [[40.64499, -73.78115],
         [40.766931, -73.982098],
         [40.77773, -73.951902],
         [40.795678, -73.971049]]
        locations = list(map(lambda marker: marker.location, markers_from_trips(cleaned_trips)))
        self.assertEqual(locations, trip_markers)

    def test_map_from(self):
        times_map = map_from([40.7589, -73.9851], 15)
        self.assertEqual(times_map.location, [40.7589, -73.9851])
        self.assertEqual(times_map.zoom_start, 15)

    def test_add_markers(self):
        cleaned_trips = [{'pickup_latitude': 40.64499, 'pickup_longitude': -73.78115, 'trip_distance': 18.38},
        {'pickup_latitude': 40.766931, 'pickup_longitude': -73.982098, 'trip_distance': 1.3},
        {'pickup_latitude': 40.77773, 'pickup_longitude': -73.951902, 'trip_distance': 4.5},
        {'pickup_latitude': 40.795678, 'pickup_longitude': -73.971049, 'trip_distance': 2.4}]
        markers = markers_from_trips(cleaned_trips)
        manhattan_map = map_from([40.7589, -73.9851], 13)
        self.assertEqual(add_markers(markers, manhattan_map), manhattan_map)

    def test_distance_location(self):
        first_trip = {'pickup_latitude': 40.64499, 'pickup_longitude': -73.78115, 'trip_distance': 18.38}
        second_trip = {'pickup_latitude': 40.766931, 'pickup_longitude': -73.982098, 'trip_distance': 1.3}
        self.assertEqual(round(distance_location(first_trip, second_trip), 3), 0.235)

    def test_distance_between_neighbors(self):
        first_trip = {'pickup_latitude': 40.64499, 'pickup_longitude': -73.78115, 'trip_distance': 18.38}
        second_trip = {'pickup_latitude': 40.766931, 'pickup_longitude': -73.982098, 'trip_distance': 1.3}
        trip_distance = {'distance_from_selected': 0.23505256047318146, 'pickup_latitude': 40.766931, 'pickup_longitude': -73.982098, 'trip_distance': 1.3}
        self.assertEqual(distance_between_neighbors(first_trip, second_trip), trip_distance)

    def test_distance_all(self):
        first_trip = {'pickup_latitude': 40.64499, 'pickup_longitude': -73.78115, 'trip_distance': 18.38}
        cleaned_trips = [{'pickup_latitude': 40.64499, 'pickup_longitude': -73.78115, 'trip_distance': 18.38},
        {'pickup_latitude': 40.766931, 'pickup_longitude': -73.982098, 'trip_distance': 1.3},
        {'pickup_latitude': 40.77773, 'pickup_longitude': -73.951902, 'trip_distance': 4.5},
        {'pickup_latitude': 40.795678, 'pickup_longitude': -73.971049, 'trip_distance': 2.4}]
        distance_trips = [{'distance_from_selected': 0.23505256047318146, 'pickup_latitude': 40.766931, 'pickup_longitude': -73.982098, 'trip_distance': 1.3},
        {'distance_from_selected': 0.2162779533470808, 'pickup_latitude': 40.77773, 'pickup_longitude': -73.951902, 'trip_distance': 4.5},
        {'distance_from_selected': 0.24242215976473674, 'pickup_latitude': 40.795678, 'pickup_longitude': -73.971049, 'trip_distance': 2.4}]
        self.assertEqual(distance_all(first_trip, cleaned_trips), distance_trips)

    def test_nearest_neighbors(self):
        new_trip = {'pickup_latitude': 40.64499, 'pickup_longitude': -73.78115, 'trip_distance': 18.38}
        trips = [{'distance_from_individual': 0.0004569288784918792, 'pickup_latitude': 40.64483, 'pickup_longitude': -73.781578, 'trip_distance': 7.78},
        {'distance_from_individual': 0.0011292165425673159, 'pickup_latitude': 40.644657, 'pickup_longitude': -73.782229, 'trip_distance': 12.7},
        {'distance_from_individual': 0.0042359798158141185, 'pickup_latitude': 40.648509, 'pickup_longitude': -73.783508, 'trip_distance': 17.3},
        {'pickup_latitude': 40.766931, 'pickup_longitude': -73.982098, 'trip_distance': 1.3, 'distance_from_individual': .5},
        {'pickup_latitude': 40.77773, 'pickup_longitude': -73.951902, 'trip_distance': 4.5, 'distance_from_individual': .09},
        {'pickup_latitude': 40.795678, 'pickup_longitude': -73.971049, 'trip_distance': 2.4, 'distance_from_individual': .08} ]
        self.assertEqual(nearest_neighbors(new_trip, trips, number = 3)[0]['trip_distance'], 7.78)
