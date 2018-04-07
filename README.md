
# Nearest Neighbors Lab

### Introduction

In this lab, you apply nearest neighbors technique to help a taxi company predict the length of their rides.  Imagine that we are hired to consult for LiftOff, a limo and taxi service that is just opening up in NYC.  Liftoff wants it's taxi drivers to target longer rides, as the longer the ride the more money it makes.  LiftOff has the following theory:

* the pickup location of a taxi ride can help predict the length of the ride.  



LiftOff asks us to do some analysis to write a function that will allow it to **predict the length of a taxi ride for any given location **.

Our technique will be the following:
  * **Collect** the data to retrieve taxi data, and only select the attributes of taxi trips that we need 
  * ** Explore ** Exampine the attributes of our data, and plot some of our data on a map
  * ** Train ** Write our nearest neighbors formula, and change the number of nearby trips to predict the length of a new trip
  * ** Predict ** Use our function to predict trip lengths of new locations

### Collect and Explore the data

#### Collect the Data

Lucky for us, if we go to [NYC Open Data](https://opendata.cityofnewyork.us/) information about NYC taxi trips is available on [it's website](https://data.cityofnewyork.us/Transportation/2014-Yellow-Taxi-Trip-Data/gn7m-em8n).

![](./nyc-taxi.png)

For you're reading pleasure, the data has already been downloaded into the [trips.json](https://github.com/learn-co-curriculum/nearest-neighbors-lab/blob/master/trips.json) file in this lab which you can find here.  We'll use Python's `json` library to take the data from the `trips.json` file and store it as a variable in our notebook.


```python
import json
# First, read the file
trips_file = open('trips.json')
# Then, convert contents to list of dictionaries 
trips = json.load(trips_file)
```

> Press shift + enter

#### Explore the data

The next step is to explore the data.  First, let's see how many trips we have.


```python
len(trips)
```




    1000



Not bad at all.  Now let's see what each individual trip looks like.  Each trip is a dictionary, so we can see the attributes of each trip with the `keys` function.


```python
trips[0].keys()
```




    dict_keys(['dropoff_datetime', 'dropoff_latitude', 'dropoff_longitude', 'fare_amount', 'imp_surcharge', 'mta_tax', 'passenger_count', 'payment_type', 'pickup_datetime', 'pickup_latitude', 'pickup_longitude', 'rate_code', 'tip_amount', 'tolls_amount', 'total_amount', 'trip_distance', 'vendor_id'])



#### Limit our data

Ok, now that we have explored some of our data, let's begin to think through what data we need for our task.

Remember that our task is to **use the trip location to predict the length of a trip**.  So let's just select the `pickup_latitude`, `pickup_longitude`, and `trip_distance` from each trip.  That will give us the trip location and related `trip_distance` for each trip.  Then based on these **actual** trip distances we can use nearest neighbors to predict an **expected** trip distance for a trip, provided an **actual** location.  

** Add in about trip distance ** 

Write a function called `parse_trips(trips)` that returns an list of the trips with only the following attributes: 
* `trip_distance`
* `pickup_latitude`
* `pickup_longitude`


```python
def parse_trips(trips):
    return list(map(lambda trip: {'trip_distance': trip['trip_distance'], 'pickup_latitude': trip['pickup_latitude'], 'pickup_longitude': trip['pickup_longitude']},trips))
```


```python
parsed_trips = parse_trips(trips)
parsed_trips and parsed_trips[0]

# {'pickup_latitude': 40.64499,
#  'pickup_longitude': -73.78115,
#  'trip_distance': 18.38}
```




    {'pickup_latitude': '40.64499',
     'pickup_longitude': '-73.781149999999997',
     'trip_distance': '18.379999999999999'}



Now, there's just one change to make.  If you look at one of the trips, all of the values are strings.  Let's change them to be integers.


```python
def float_values(trips):    
    return trips and list(map(lambda trip: {'trip_distance': float(trip['trip_distance']), 'pickup_latitude': float(trip['pickup_latitude']), 'pickup_longitude': float(trip['pickup_longitude'])},trips))
```


```python
cleaned_trips = float_values(parsed_trips)
```


```python
cleaned_trips[0]
```




    {'pickup_latitude': 40.64499,
     'pickup_longitude': -73.78115,
     'trip_distance': 18.38}



### Exploring the Data

Now that we have paired down our data, let's get a sense of our trip data.  We can use the `folium` Python library to plot a map of Manhattan, and our data.  We import `folium`, and then use the `Map` function to pass through a `location`, and `zoom_start`.


```python
import folium
manhattan_map = folium.Map(location=[40.7589, -73.9851], zoom_start=11)
```


```python
manhattan_map
```




<div style="width:100%;"><div style="position:relative;width:100%;height:0;padding-bottom:60%;"><iframe src="data:text/html;charset=utf-8;base64,PCFET0NUWVBFIGh0bWw+CjxoZWFkPiAgICAKICAgIDxtZXRhIGh0dHAtZXF1aXY9ImNvbnRlbnQtdHlwZSIgY29udGVudD0idGV4dC9odG1sOyBjaGFyc2V0PVVURi04IiAvPgogICAgPHNjcmlwdD5MX1BSRUZFUl9DQU5WQVMgPSBmYWxzZTsgTF9OT19UT1VDSCA9IGZhbHNlOyBMX0RJU0FCTEVfM0QgPSBmYWxzZTs8L3NjcmlwdD4KICAgIDxzY3JpcHQgc3JjPSJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvbnBtL2xlYWZsZXRAMS4yLjAvZGlzdC9sZWFmbGV0LmpzIj48L3NjcmlwdD4KICAgIDxzY3JpcHQgc3JjPSJodHRwczovL2FqYXguZ29vZ2xlYXBpcy5jb20vYWpheC9saWJzL2pxdWVyeS8xLjExLjEvanF1ZXJ5Lm1pbi5qcyI+PC9zY3JpcHQ+CiAgICA8c2NyaXB0IHNyYz0iaHR0cHM6Ly9tYXhjZG4uYm9vdHN0cmFwY2RuLmNvbS9ib290c3RyYXAvMy4yLjAvanMvYm9vdHN0cmFwLm1pbi5qcyI+PC9zY3JpcHQ+CiAgICA8c2NyaXB0IHNyYz0iaHR0cHM6Ly9jZG5qcy5jbG91ZGZsYXJlLmNvbS9hamF4L2xpYnMvTGVhZmxldC5hd2Vzb21lLW1hcmtlcnMvMi4wLjIvbGVhZmxldC5hd2Vzb21lLW1hcmtlcnMuanMiPjwvc2NyaXB0PgogICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvbnBtL2xlYWZsZXRAMS4yLjAvZGlzdC9sZWFmbGV0LmNzcyIgLz4KICAgIDxsaW5rIHJlbD0ic3R5bGVzaGVldCIgaHJlZj0iaHR0cHM6Ly9tYXhjZG4uYm9vdHN0cmFwY2RuLmNvbS9ib290c3RyYXAvMy4yLjAvY3NzL2Jvb3RzdHJhcC5taW4uY3NzIiAvPgogICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJodHRwczovL21heGNkbi5ib290c3RyYXBjZG4uY29tL2Jvb3RzdHJhcC8zLjIuMC9jc3MvYm9vdHN0cmFwLXRoZW1lLm1pbi5jc3MiIC8+CiAgICA8bGluayByZWw9InN0eWxlc2hlZXQiIGhyZWY9Imh0dHBzOi8vbWF4Y2RuLmJvb3RzdHJhcGNkbi5jb20vZm9udC1hd2Vzb21lLzQuNi4zL2Nzcy9mb250LWF3ZXNvbWUubWluLmNzcyIgLz4KICAgIDxsaW5rIHJlbD0ic3R5bGVzaGVldCIgaHJlZj0iaHR0cHM6Ly9jZG5qcy5jbG91ZGZsYXJlLmNvbS9hamF4L2xpYnMvTGVhZmxldC5hd2Vzb21lLW1hcmtlcnMvMi4wLjIvbGVhZmxldC5hd2Vzb21lLW1hcmtlcnMuY3NzIiAvPgogICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJodHRwczovL3Jhd2dpdC5jb20vcHl0aG9uLXZpc3VhbGl6YXRpb24vZm9saXVtL21hc3Rlci9mb2xpdW0vdGVtcGxhdGVzL2xlYWZsZXQuYXdlc29tZS5yb3RhdGUuY3NzIiAvPgogICAgPHN0eWxlPmh0bWwsIGJvZHkge3dpZHRoOiAxMDAlO2hlaWdodDogMTAwJTttYXJnaW46IDA7cGFkZGluZzogMDt9PC9zdHlsZT4KICAgIDxzdHlsZT4jbWFwIHtwb3NpdGlvbjphYnNvbHV0ZTt0b3A6MDtib3R0b206MDtyaWdodDowO2xlZnQ6MDt9PC9zdHlsZT4KICAgIAogICAgICAgICAgICA8c3R5bGU+ICNtYXBfNWJlNmE3ODE3YWU3NGZhYTg4NzcyNDM1ZDFlMjZmZGQgewogICAgICAgICAgICAgICAgcG9zaXRpb24gOiByZWxhdGl2ZTsKICAgICAgICAgICAgICAgIHdpZHRoIDogMTAwLjAlOwogICAgICAgICAgICAgICAgaGVpZ2h0OiAxMDAuMCU7CiAgICAgICAgICAgICAgICBsZWZ0OiAwLjAlOwogICAgICAgICAgICAgICAgdG9wOiAwLjAlOwogICAgICAgICAgICAgICAgfQogICAgICAgICAgICA8L3N0eWxlPgogICAgICAgIAo8L2hlYWQ+Cjxib2R5PiAgICAKICAgIAogICAgICAgICAgICA8ZGl2IGNsYXNzPSJmb2xpdW0tbWFwIiBpZD0ibWFwXzViZTZhNzgxN2FlNzRmYWE4ODc3MjQzNWQxZTI2ZmRkIiA+PC9kaXY+CiAgICAgICAgCjwvYm9keT4KPHNjcmlwdD4gICAgCiAgICAKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGJvdW5kcyA9IG51bGw7CiAgICAgICAgICAgIAoKICAgICAgICAgICAgdmFyIG1hcF81YmU2YTc4MTdhZTc0ZmFhODg3NzI0MzVkMWUyNmZkZCA9IEwubWFwKAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgJ21hcF81YmU2YTc4MTdhZTc0ZmFhODg3NzI0MzVkMWUyNmZkZCcsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7Y2VudGVyOiBbNDAuNzU4OSwtNzMuOTg1MV0sCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB6b29tOiAxMSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIG1heEJvdW5kczogYm91bmRzLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgbGF5ZXJzOiBbXSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHdvcmxkQ29weUp1bXA6IGZhbHNlLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgY3JzOiBMLkNSUy5FUFNHMzg1NwogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB9KTsKICAgICAgICAgICAgCiAgICAgICAgCiAgICAKICAgICAgICAgICAgdmFyIHRpbGVfbGF5ZXJfZDdkNDFkNTRjZjFjNDg4MGExNWE5ZDA1NzRjYTQ1MWQgPSBMLnRpbGVMYXllcigKICAgICAgICAgICAgICAgICdodHRwczovL3tzfS50aWxlLm9wZW5zdHJlZXRtYXAub3JnL3t6fS97eH0ve3l9LnBuZycsCiAgICAgICAgICAgICAgICB7CiAgImF0dHJpYnV0aW9uIjogbnVsbCwKICAiZGV0ZWN0UmV0aW5hIjogZmFsc2UsCiAgIm1heFpvb20iOiAxOCwKICAibWluWm9vbSI6IDEsCiAgIm5vV3JhcCI6IGZhbHNlLAogICJzdWJkb21haW5zIjogImFiYyIKfQogICAgICAgICAgICAgICAgKS5hZGRUbyhtYXBfNWJlNmE3ODE3YWU3NGZhYTg4NzcyNDM1ZDFlMjZmZGQpOwogICAgICAgIAo8L3NjcmlwdD4=" style="position:absolute;width:100%;height:100%;left:0;top:0;border:none !important;" allowfullscreen webkitallowfullscreen mozallowfullscreen></iframe></div></div>



Ok, now let's see how we could add a dot to mark a specific location.  We'll start with Times Square.


```python
marker = folium.CircleMarker(location = [40.7589, -73.9851], radius=10)
marker.add_to(manhattan_map)
```




    <folium.features.CircleMarker at 0x11987ea90>



Above, we first create a marker.  Then we add that circle marker to the `manhattan_map` we created earlier. 


```python
manhattan_map
```




<div style="width:100%;"><div style="position:relative;width:100%;height:0;padding-bottom:60%;"><iframe src="data:text/html;charset=utf-8;base64,PCFET0NUWVBFIGh0bWw+CjxoZWFkPiAgICAKICAgIDxtZXRhIGh0dHAtZXF1aXY9ImNvbnRlbnQtdHlwZSIgY29udGVudD0idGV4dC9odG1sOyBjaGFyc2V0PVVURi04IiAvPgogICAgPHNjcmlwdD5MX1BSRUZFUl9DQU5WQVMgPSBmYWxzZTsgTF9OT19UT1VDSCA9IGZhbHNlOyBMX0RJU0FCTEVfM0QgPSBmYWxzZTs8L3NjcmlwdD4KICAgIDxzY3JpcHQgc3JjPSJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvbnBtL2xlYWZsZXRAMS4yLjAvZGlzdC9sZWFmbGV0LmpzIj48L3NjcmlwdD4KICAgIDxzY3JpcHQgc3JjPSJodHRwczovL2FqYXguZ29vZ2xlYXBpcy5jb20vYWpheC9saWJzL2pxdWVyeS8xLjExLjEvanF1ZXJ5Lm1pbi5qcyI+PC9zY3JpcHQ+CiAgICA8c2NyaXB0IHNyYz0iaHR0cHM6Ly9tYXhjZG4uYm9vdHN0cmFwY2RuLmNvbS9ib290c3RyYXAvMy4yLjAvanMvYm9vdHN0cmFwLm1pbi5qcyI+PC9zY3JpcHQ+CiAgICA8c2NyaXB0IHNyYz0iaHR0cHM6Ly9jZG5qcy5jbG91ZGZsYXJlLmNvbS9hamF4L2xpYnMvTGVhZmxldC5hd2Vzb21lLW1hcmtlcnMvMi4wLjIvbGVhZmxldC5hd2Vzb21lLW1hcmtlcnMuanMiPjwvc2NyaXB0PgogICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvbnBtL2xlYWZsZXRAMS4yLjAvZGlzdC9sZWFmbGV0LmNzcyIgLz4KICAgIDxsaW5rIHJlbD0ic3R5bGVzaGVldCIgaHJlZj0iaHR0cHM6Ly9tYXhjZG4uYm9vdHN0cmFwY2RuLmNvbS9ib290c3RyYXAvMy4yLjAvY3NzL2Jvb3RzdHJhcC5taW4uY3NzIiAvPgogICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJodHRwczovL21heGNkbi5ib290c3RyYXBjZG4uY29tL2Jvb3RzdHJhcC8zLjIuMC9jc3MvYm9vdHN0cmFwLXRoZW1lLm1pbi5jc3MiIC8+CiAgICA8bGluayByZWw9InN0eWxlc2hlZXQiIGhyZWY9Imh0dHBzOi8vbWF4Y2RuLmJvb3RzdHJhcGNkbi5jb20vZm9udC1hd2Vzb21lLzQuNi4zL2Nzcy9mb250LWF3ZXNvbWUubWluLmNzcyIgLz4KICAgIDxsaW5rIHJlbD0ic3R5bGVzaGVldCIgaHJlZj0iaHR0cHM6Ly9jZG5qcy5jbG91ZGZsYXJlLmNvbS9hamF4L2xpYnMvTGVhZmxldC5hd2Vzb21lLW1hcmtlcnMvMi4wLjIvbGVhZmxldC5hd2Vzb21lLW1hcmtlcnMuY3NzIiAvPgogICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJodHRwczovL3Jhd2dpdC5jb20vcHl0aG9uLXZpc3VhbGl6YXRpb24vZm9saXVtL21hc3Rlci9mb2xpdW0vdGVtcGxhdGVzL2xlYWZsZXQuYXdlc29tZS5yb3RhdGUuY3NzIiAvPgogICAgPHN0eWxlPmh0bWwsIGJvZHkge3dpZHRoOiAxMDAlO2hlaWdodDogMTAwJTttYXJnaW46IDA7cGFkZGluZzogMDt9PC9zdHlsZT4KICAgIDxzdHlsZT4jbWFwIHtwb3NpdGlvbjphYnNvbHV0ZTt0b3A6MDtib3R0b206MDtyaWdodDowO2xlZnQ6MDt9PC9zdHlsZT4KICAgIAogICAgICAgICAgICA8c3R5bGU+ICNtYXBfMTFhMjNjOTY4NGJmNDVhMjlmZGUwYTBiYmNkMjk1MDAgewogICAgICAgICAgICAgICAgcG9zaXRpb24gOiByZWxhdGl2ZTsKICAgICAgICAgICAgICAgIHdpZHRoIDogMTAwLjAlOwogICAgICAgICAgICAgICAgaGVpZ2h0OiAxMDAuMCU7CiAgICAgICAgICAgICAgICBsZWZ0OiAwLjAlOwogICAgICAgICAgICAgICAgdG9wOiAwLjAlOwogICAgICAgICAgICAgICAgfQogICAgICAgICAgICA8L3N0eWxlPgogICAgICAgIAo8L2hlYWQ+Cjxib2R5PiAgICAKICAgIAogICAgICAgICAgICA8ZGl2IGNsYXNzPSJmb2xpdW0tbWFwIiBpZD0ibWFwXzExYTIzYzk2ODRiZjQ1YTI5ZmRlMGEwYmJjZDI5NTAwIiA+PC9kaXY+CiAgICAgICAgCjwvYm9keT4KPHNjcmlwdD4gICAgCiAgICAKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGJvdW5kcyA9IG51bGw7CiAgICAgICAgICAgIAoKICAgICAgICAgICAgdmFyIG1hcF8xMWEyM2M5Njg0YmY0NWEyOWZkZTBhMGJiY2QyOTUwMCA9IEwubWFwKAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgJ21hcF8xMWEyM2M5Njg0YmY0NWEyOWZkZTBhMGJiY2QyOTUwMCcsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7Y2VudGVyOiBbNDAuNzU4OSwtNzMuOTg1MV0sCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB6b29tOiAxMSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIG1heEJvdW5kczogYm91bmRzLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgbGF5ZXJzOiBbXSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHdvcmxkQ29weUp1bXA6IGZhbHNlLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgY3JzOiBMLkNSUy5FUFNHMzg1NwogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB9KTsKICAgICAgICAgICAgCiAgICAgICAgCiAgICAKICAgICAgICAgICAgdmFyIHRpbGVfbGF5ZXJfOWE5NDVjYTM4MzE0NGFjMmEwNDExYzJiNTZmNzViNmQgPSBMLnRpbGVMYXllcigKICAgICAgICAgICAgICAgICdodHRwczovL3tzfS50aWxlLm9wZW5zdHJlZXRtYXAub3JnL3t6fS97eH0ve3l9LnBuZycsCiAgICAgICAgICAgICAgICB7CiAgImF0dHJpYnV0aW9uIjogbnVsbCwKICAiZGV0ZWN0UmV0aW5hIjogZmFsc2UsCiAgIm1heFpvb20iOiAxOCwKICAibWluWm9vbSI6IDEsCiAgIm5vV3JhcCI6IGZhbHNlLAogICJzdWJkb21haW5zIjogImFiYyIKfQogICAgICAgICAgICAgICAgKS5hZGRUbyhtYXBfMTFhMjNjOTY4NGJmNDVhMjlmZGUwYTBiYmNkMjk1MDApOwogICAgICAgIAogICAgCiAgICAgICAgICAgIHZhciBjaXJjbGVfbWFya2VyXzUxYTliNDFmNzZiZTQzMDk4ZjlhNmJjOWUxNzQ4ZGYzID0gTC5jaXJjbGVNYXJrZXIoCiAgICAgICAgICAgICAgICBbNDAuNzU4OSwtNzMuOTg1MV0sCiAgICAgICAgICAgICAgICB7CiAgImJ1YmJsaW5nTW91c2VFdmVudHMiOiB0cnVlLAogICJjb2xvciI6ICIjMzM4OGZmIiwKICAiZGFzaEFycmF5IjogbnVsbCwKICAiZGFzaE9mZnNldCI6IG51bGwsCiAgImZpbGwiOiBmYWxzZSwKICAiZmlsbENvbG9yIjogIiMzMzg4ZmYiLAogICJmaWxsT3BhY2l0eSI6IDAuMiwKICAiZmlsbFJ1bGUiOiAiZXZlbm9kZCIsCiAgImxpbmVDYXAiOiAicm91bmQiLAogICJsaW5lSm9pbiI6ICJyb3VuZCIsCiAgIm9wYWNpdHkiOiAxLjAsCiAgInJhZGl1cyI6IDEwLAogICJzdHJva2UiOiB0cnVlLAogICJ3ZWlnaHQiOiAzCn0KICAgICAgICAgICAgICAgICkuYWRkVG8obWFwXzExYTIzYzk2ODRiZjQ1YTI5ZmRlMGEwYmJjZDI5NTAwKTsKICAgICAgICAgICAgCjwvc2NyaXB0Pg==" style="position:absolute;width:100%;height:100%;left:0;top:0;border:none !important;" allowfullscreen webkitallowfullscreen mozallowfullscreen></iframe></div></div>



Do you see that blue dot near Time's Square?  That is our marker.  

So now thar we can plot one marker on a map, we should have a sense of how we can plot many markers on a map to display our taxi ride data.  We simply plot a map, and then we add a marker for each location of a taxi trip.

So now let's write some functions to allow us to plot maps and add markers a little more easily.  

#### Writing some map plotting functions

As a first step towards this, note that the functions to create both a marker and map each take in a location as two element list, representing the latitude and longitude values.  Take another look:

```python
marker = folium.CircleMarker(location = [40.7589, -73.9851])
manhattan_map = folium.Map(location=[40.7589, -73.9851])
```

So let's write a function called to create this two element list from a trip.  Write a function called `location` that  takes in a trip as an argument and returns a list where the first element is the latitude and the second is the longitude.  Remember that a location looks like the following:


```python
first_trip = {'pickup_latitude': 40.64499, 'pickup_longitude': -73.78115,  'trip_distance': 18.38}
first_trip
```




    {'pickup_latitude': 40.64499,
     'pickup_longitude': -73.78115,
     'trip_distance': 18.38}




```python
def location(trip):
    return [trip['pickup_latitude'], trip['pickup_longitude']]
```


```python
first_location = location(first_trip) # [40.64499, -73.78115]
first_location # [40.64499, -73.78115]
```




    [40.64499, -73.78115]



Ok, now that we can turn a trip into a location, let's turn a location into a marker.  Write a function called `to_marker` that takes in a location (in the form of a list) as an argument, and returns a folium `circleMarker` for that location.  The radius of the marker should always equal 6.


```python
def to_marker(location):
    return folium.CircleMarker(location, radius = 6)
```


```python
import json
times_square_marker = to_marker([40.7589, -73.9851])

times_square_marker and times_square_marker.location # [40.7589, -73.9851]
times_square_marker and json.loads(times_square_marker.options)['radius'] # 6
```




    6



Ok, now that we know how to produce a single marker, let's write a function to produce lots.  We can write a function called `markers_from_trips` that takes in a list of trips, and returns a marker object for each trip.  


```python
def markers_from_trips(trips):
    locations = list(map(lambda trip: location(trip), trips))
    return list(map(lambda location: to_marker(location),locations))
```


```python
trip_markers = markers_from_trips(cleaned_trips)
```


```python
trip_markers and len(trip_markers) # 1000

marker_locations = None

if trip_markers:  
    marker_locations = list(map(lambda marker: marker.location ,trip_markers))

trip_markers and marker_locations == list(map(lambda trip: location(trip), cleaned_trips)) # True
```




    True



Ok, now that we have a function that creates locations, and a function that creates markers, it is time to write a function to plot a map. 

Write a function called `map_from` that, provided the first argument of a list location and second argument an integer representing the `zoom_start`, returns a `folium` map the corresponding location and `zoom_start` attributes.

> Hint: The following is to write a map with folium:
> ```python 
    folium.Map(location=location, zoom_start=zoom_amount)
> ```


```python
def map_from(location, zoom_amount):
    return folium.Map(location=location, zoom_start=zoom_amount)
```


```python
times_square_map = map_from([40.7589, -73.9851], 15)
times_square_map and times_square_map.location # [40.7589, -73.9851]
times_square_map and times_square_map.zoom_start # 15
```




    15




```python
times_square_marker and times_square_marker.add_to(times_square_map)
times_square_map
```




<div style="width:100%;"><div style="position:relative;width:100%;height:0;padding-bottom:60%;"><iframe src="data:text/html;charset=utf-8;base64,PCFET0NUWVBFIGh0bWw+CjxoZWFkPiAgICAKICAgIDxtZXRhIGh0dHAtZXF1aXY9ImNvbnRlbnQtdHlwZSIgY29udGVudD0idGV4dC9odG1sOyBjaGFyc2V0PVVURi04IiAvPgogICAgPHNjcmlwdD5MX1BSRUZFUl9DQU5WQVMgPSBmYWxzZTsgTF9OT19UT1VDSCA9IGZhbHNlOyBMX0RJU0FCTEVfM0QgPSBmYWxzZTs8L3NjcmlwdD4KICAgIDxzY3JpcHQgc3JjPSJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvbnBtL2xlYWZsZXRAMS4yLjAvZGlzdC9sZWFmbGV0LmpzIj48L3NjcmlwdD4KICAgIDxzY3JpcHQgc3JjPSJodHRwczovL2FqYXguZ29vZ2xlYXBpcy5jb20vYWpheC9saWJzL2pxdWVyeS8xLjExLjEvanF1ZXJ5Lm1pbi5qcyI+PC9zY3JpcHQ+CiAgICA8c2NyaXB0IHNyYz0iaHR0cHM6Ly9tYXhjZG4uYm9vdHN0cmFwY2RuLmNvbS9ib290c3RyYXAvMy4yLjAvanMvYm9vdHN0cmFwLm1pbi5qcyI+PC9zY3JpcHQ+CiAgICA8c2NyaXB0IHNyYz0iaHR0cHM6Ly9jZG5qcy5jbG91ZGZsYXJlLmNvbS9hamF4L2xpYnMvTGVhZmxldC5hd2Vzb21lLW1hcmtlcnMvMi4wLjIvbGVhZmxldC5hd2Vzb21lLW1hcmtlcnMuanMiPjwvc2NyaXB0PgogICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvbnBtL2xlYWZsZXRAMS4yLjAvZGlzdC9sZWFmbGV0LmNzcyIgLz4KICAgIDxsaW5rIHJlbD0ic3R5bGVzaGVldCIgaHJlZj0iaHR0cHM6Ly9tYXhjZG4uYm9vdHN0cmFwY2RuLmNvbS9ib290c3RyYXAvMy4yLjAvY3NzL2Jvb3RzdHJhcC5taW4uY3NzIiAvPgogICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJodHRwczovL21heGNkbi5ib290c3RyYXBjZG4uY29tL2Jvb3RzdHJhcC8zLjIuMC9jc3MvYm9vdHN0cmFwLXRoZW1lLm1pbi5jc3MiIC8+CiAgICA8bGluayByZWw9InN0eWxlc2hlZXQiIGhyZWY9Imh0dHBzOi8vbWF4Y2RuLmJvb3RzdHJhcGNkbi5jb20vZm9udC1hd2Vzb21lLzQuNi4zL2Nzcy9mb250LWF3ZXNvbWUubWluLmNzcyIgLz4KICAgIDxsaW5rIHJlbD0ic3R5bGVzaGVldCIgaHJlZj0iaHR0cHM6Ly9jZG5qcy5jbG91ZGZsYXJlLmNvbS9hamF4L2xpYnMvTGVhZmxldC5hd2Vzb21lLW1hcmtlcnMvMi4wLjIvbGVhZmxldC5hd2Vzb21lLW1hcmtlcnMuY3NzIiAvPgogICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJodHRwczovL3Jhd2dpdC5jb20vcHl0aG9uLXZpc3VhbGl6YXRpb24vZm9saXVtL21hc3Rlci9mb2xpdW0vdGVtcGxhdGVzL2xlYWZsZXQuYXdlc29tZS5yb3RhdGUuY3NzIiAvPgogICAgPHN0eWxlPmh0bWwsIGJvZHkge3dpZHRoOiAxMDAlO2hlaWdodDogMTAwJTttYXJnaW46IDA7cGFkZGluZzogMDt9PC9zdHlsZT4KICAgIDxzdHlsZT4jbWFwIHtwb3NpdGlvbjphYnNvbHV0ZTt0b3A6MDtib3R0b206MDtyaWdodDowO2xlZnQ6MDt9PC9zdHlsZT4KICAgIAogICAgICAgICAgICA8c3R5bGU+ICNtYXBfNjZlNzUxY2IzNTllNDYyY2E5ZWMxMGU1NmVmZGI3ZTQgewogICAgICAgICAgICAgICAgcG9zaXRpb24gOiByZWxhdGl2ZTsKICAgICAgICAgICAgICAgIHdpZHRoIDogMTAwLjAlOwogICAgICAgICAgICAgICAgaGVpZ2h0OiAxMDAuMCU7CiAgICAgICAgICAgICAgICBsZWZ0OiAwLjAlOwogICAgICAgICAgICAgICAgdG9wOiAwLjAlOwogICAgICAgICAgICAgICAgfQogICAgICAgICAgICA8L3N0eWxlPgogICAgICAgIAo8L2hlYWQ+Cjxib2R5PiAgICAKICAgIAogICAgICAgICAgICA8ZGl2IGNsYXNzPSJmb2xpdW0tbWFwIiBpZD0ibWFwXzY2ZTc1MWNiMzU5ZTQ2MmNhOWVjMTBlNTZlZmRiN2U0IiA+PC9kaXY+CiAgICAgICAgCjwvYm9keT4KPHNjcmlwdD4gICAgCiAgICAKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGJvdW5kcyA9IG51bGw7CiAgICAgICAgICAgIAoKICAgICAgICAgICAgdmFyIG1hcF82NmU3NTFjYjM1OWU0NjJjYTllYzEwZTU2ZWZkYjdlNCA9IEwubWFwKAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgJ21hcF82NmU3NTFjYjM1OWU0NjJjYTllYzEwZTU2ZWZkYjdlNCcsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7Y2VudGVyOiBbNDAuNzU4OSwtNzMuOTg1MV0sCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB6b29tOiAxNSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIG1heEJvdW5kczogYm91bmRzLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgbGF5ZXJzOiBbXSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHdvcmxkQ29weUp1bXA6IGZhbHNlLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgY3JzOiBMLkNSUy5FUFNHMzg1NwogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB9KTsKICAgICAgICAgICAgCiAgICAgICAgCiAgICAKICAgICAgICAgICAgdmFyIHRpbGVfbGF5ZXJfYTA1ZWM2MTcxZGNlNDdiNGFmMjIxZTZlZjdlZDQyZmIgPSBMLnRpbGVMYXllcigKICAgICAgICAgICAgICAgICdodHRwczovL3tzfS50aWxlLm9wZW5zdHJlZXRtYXAub3JnL3t6fS97eH0ve3l9LnBuZycsCiAgICAgICAgICAgICAgICB7CiAgImF0dHJpYnV0aW9uIjogbnVsbCwKICAiZGV0ZWN0UmV0aW5hIjogZmFsc2UsCiAgIm1heFpvb20iOiAxOCwKICAibWluWm9vbSI6IDEsCiAgIm5vV3JhcCI6IGZhbHNlLAogICJzdWJkb21haW5zIjogImFiYyIKfQogICAgICAgICAgICAgICAgKS5hZGRUbyhtYXBfNjZlNzUxY2IzNTllNDYyY2E5ZWMxMGU1NmVmZGI3ZTQpOwogICAgICAgIAogICAgCiAgICAgICAgICAgIHZhciBjaXJjbGVfbWFya2VyXzc2YzJiNGEzNzUyMDQ4ODZhYTZiNmYwN2I1ZTM0ZGI2ID0gTC5jaXJjbGVNYXJrZXIoCiAgICAgICAgICAgICAgICBbNDAuNzU4OSwtNzMuOTg1MV0sCiAgICAgICAgICAgICAgICB7CiAgImJ1YmJsaW5nTW91c2VFdmVudHMiOiB0cnVlLAogICJjb2xvciI6ICIjMzM4OGZmIiwKICAiZGFzaEFycmF5IjogbnVsbCwKICAiZGFzaE9mZnNldCI6IG51bGwsCiAgImZpbGwiOiBmYWxzZSwKICAiZmlsbENvbG9yIjogIiMzMzg4ZmYiLAogICJmaWxsT3BhY2l0eSI6IDAuMiwKICAiZmlsbFJ1bGUiOiAiZXZlbm9kZCIsCiAgImxpbmVDYXAiOiAicm91bmQiLAogICJsaW5lSm9pbiI6ICJyb3VuZCIsCiAgIm9wYWNpdHkiOiAxLjAsCiAgInJhZGl1cyI6IDYsCiAgInN0cm9rZSI6IHRydWUsCiAgIndlaWdodCI6IDMKfQogICAgICAgICAgICAgICAgKS5hZGRUbyhtYXBfNjZlNzUxY2IzNTllNDYyY2E5ZWMxMGU1NmVmZGI3ZTQpOwogICAgICAgICAgICAKPC9zY3JpcHQ+" style="position:absolute;width:100%;height:100%;left:0;top:0;border:none !important;" allowfullscreen webkitallowfullscreen mozallowfullscreen></iframe></div></div>



Now that we have a marker and a map, now let's write a function that adds a lot of markers to a map.


```python
manhattan_map = map_from([40.7589, -73.9851], 13)
```


```python
def add_markers(markers, map_obj):
    for marker in markers:
        marker.add_to(map_obj)
    return map_obj
```


```python
map_with_markers = add_markers(trip_markers, manhattan_map)
```


```python
map_with_markers
```




    <bound method Map.choropleth of <folium.folium.Map object at 0x10b7aa1d0>>



### Using Nearest Neighbors

Ok, let's write a function that given a latitude and longitude will predict the fare distance for us.  We'll do this by first finding the nearest trips given a latitude and longitude. 

 As a first step, write a function named `distance_location` that calculates the distance in pickup location between two trips.


```python
import math

def distance_location(selected_trip, neighbor_trip):
    distance_squared = (neighbor_trip['pickup_latitude'] - selected_trip['pickup_latitude'])**2 + (neighbor_trip['pickup_longitude'] - selected_trip['pickup_longitude'])**2
    return math.sqrt(distance_squared)
```


```python
first_trip = {'pickup_latitude': 40.64499, 'pickup_longitude': -73.78115, 'trip_distance': 18.38}
second_trip = {'pickup_latitude': 40.766931, 'pickup_longitude': -73.982098, 'trip_distance': 1.3}
distance_first_and_second = distance_location(first_trip, second_trip)

distance_first_and_second and round(distance_first_and_second, 3) # 0.235
```




    0.235



Ok, next write a function called `distance_between_neighbors` that adds a new key-value pair, called `distance_from_selected`, that calculates the distance of the `neighbor_trip` from the `selected_trip`.


```python
def distance_between_neighbors(selected_trip, neighbor_trip):
    neighbor_with_distance = neighbor_trip.copy()
    neighbor_with_distance['distance_from_selected'] = distance_location(selected_trip, neighbor_trip)
    return neighbor_with_distance
```


```python
distance_between_neighbors(first_trip, second_trip)

# {'distance_from_individual': 0.23505256047318146,
#  'pickup_latitude': 40.766931,
#  'pickup_longitude': -73.982098,
#  'trip_distance': 1.3}
```




    {'distance_from_selected': 0.23505256047318146,
     'pickup_latitude': 40.766931,
     'pickup_longitude': -73.982098,
     'trip_distance': 1.3}



Ok, now our neighbor_trip has another attribute called `distance_from_selected`, that indicates the distance from the `neighbor_trip`'s pickup location from the `selected_trip`.

> ** Understand the data:** Our dictionary now has a few attributes, two of which say distance.  Let's make sure we understand the difference. 
> * **`distance_from_selected`:** This is our calculation of the distance of the neighbor's pickup location from the selected trip.
> * **`trip_distance`:** This is the attribute we were provided initially.  It tells us the length of the neighbor's taxi trip from pickup to dropoff.  

Next, write a function called `distance_all` that provided a list of neighbors, returns each of those neighbors with their respective `distance_from_individual` numbers.


```python
def distance_all(selected_individual, neighbors):
    remaining_neighbors = filter(lambda neighbor: neighbor != selected_individual, neighbors)
    return list(map(lambda neighbor: distance_between_neighbors(selected_individual, neighbor), remaining_neighbors))
```


```python
cleaned_trips and distance_all(first_trip, cleaned_trips[0:4])
```

Now write the nearest neighbors formula to calculate the distance of the `selected_trip` from all of the `cleaned_trips` in our dataset.  If no number is provided, it should return the top 3 neighbors.


```python
def nearest_neighbors(selected_trip, trips, number = 3):
    neighbor_distances = distance_all(selected_trip, trips)
    sorted_neighbors = sorted(neighbor_distances, key=lambda neighbor: neighbor['distance_from_selected'])
    return sorted_neighbors[:number]
```


```python
new_trip = {'pickup_latitude': 40.64499,
'pickup_longitude': -73.78115,
'trip_distance': 18.38}

nearest_three_neighbors = nearest_neighbors(new_trip, cleaned_trips or [], number = 3)
nearest_three_neighbors
# [{'distance_from_individual': 0.0004569288784918792,
#   'pickup_latitude': 40.64483,
#   'pickup_longitude': -73.781578,
#   'trip_distance': 7.78},
#  {'distance_from_individual': 0.0011292165425673159,
#   'pickup_latitude': 40.644657,
#   'pickup_longitude': -73.782229,
#   'trip_distance': 12.7},
#  {'distance_from_individual': 0.0042359798158141185,
#   'pickup_latitude': 40.648509,
#   'pickup_longitude': -73.783508,
#   'trip_distance': 17.3}]
```




    [{'distance_from_selected': 0.0004569288784918792,
      'pickup_latitude': 40.64483,
      'pickup_longitude': -73.781578,
      'trip_distance': 7.78},
     {'distance_from_selected': 0.0011292165425673159,
      'pickup_latitude': 40.644657,
      'pickup_longitude': -73.782229,
      'trip_distance': 12.7},
     {'distance_from_selected': 0.0042359798158141185,
      'pickup_latitude': 40.648509,
      'pickup_longitude': -73.783508,
      'trip_distance': 17.3}]



Ok great! Now that we can provide a new trip location, and find the distances of the three nearest trips, we can take  calculate an estimate of the trip distance for that new trip location.  

We do so simply by calculating an average of it's nearest neighbors.


```python
import statistics
def median_distance(neighbors):
    nearest_distances = list(map(lambda neighbor: neighbor['trip_distance'], neighbors))
    return round(statistics.median(nearest_distances), 3)


nearest_three_neighbors = nearest_neighbors(new_trip, cleaned_trips or [], number = 3)
distance_estimate_of_selected_trip = mean_distance(nearest_three_neighbors) # 12.593
```

### Choosing the correct number of neighbors

Now, as we know from the last lesson, one tricky element is to determine how many neighbors to choose, our $k$ value,  before calculating the average.  We want to choose our value of $k$ such that it properly matches actual data, and so that it applies to new data.  There are fancy formulas to ensure that we **train** our algorithm so that our formula is optimized for all data, but here let's see different $k$ values manually.  This is the gist of choosing our $k$ value:

* If we choose a $k$ value too low, our formula will be too heavily influenced by a single neighbor, whereas if our $k$ value is too high, we will be choosing so many neighbors that our nearest neighbors formula will not be adjust enough according to locations.

Ok, let's experiment with this.

First, let's choose a midtown location, to see what the trip distance would be.  A Google search reveals the coordinates of 51st and 7th avenue to be the following.


```python
midtown_trip = dict(pickup_latitude=40.761710, pickup_longitude=-73.982760)
```


```python
seven_closest = nearest_neighbors(midtown_trip, cleaned_trips, number = 12)
seven_closest
```




    [{'distance_from_selected': 0.00037310588309379025,
      'pickup_latitude': 40.761372,
      'pickup_longitude': -73.982602,
      'trip_distance': 0.58},
     {'distance_from_selected': 0.00080072217404248,
      'pickup_latitude': 40.762444,
      'pickup_longitude': -73.98244,
      'trip_distance': 0.8},
     {'distance_from_selected': 0.0011555682584735844,
      'pickup_latitude': 40.762767,
      'pickup_longitude': -73.982293,
      'trip_distance': 1.4},
     {'distance_from_selected': 0.0012508768924205918,
      'pickup_latitude': 40.762868,
      'pickup_longitude': -73.983233,
      'trip_distance': 8.3},
     {'distance_from_selected': 0.0018118976240381972,
      'pickup_latitude': 40.760057,
      'pickup_longitude': -73.983502,
      'trip_distance': 1.26},
     {'distance_from_selected': 0.002067074502774709,
      'pickup_latitude': 40.760644,
      'pickup_longitude': -73.984531,
      'trip_distance': 0.0},
     {'distance_from_selected': 0.0020684557041472677,
      'pickup_latitude': 40.762107,
      'pickup_longitude': -73.98479,
      'trip_distance': 1.72},
     {'distance_from_selected': 0.0024634057725016426,
      'pickup_latitude': 40.760442,
      'pickup_longitude': -73.980648,
      'trip_distance': 12.7},
     {'distance_from_selected': 0.00250734760254793,
      'pickup_latitude': 40.763684,
      'pickup_longitude': -73.981214,
      'trip_distance': 2.1},
     {'distance_from_selected': 0.002609860149511136,
      'pickup_latitude': 40.759663,
      'pickup_longitude': -73.981141,
      'trip_distance': 2.2},
     {'distance_from_selected': 0.0026676605856094052,
      'pickup_latitude': 40.759347,
      'pickup_longitude': -73.981522,
      'trip_distance': 2.73},
     {'distance_from_selected': 0.0028054840937036273,
      'pickup_latitude': 40.75906,
      'pickup_longitude': -73.983681,
      'trip_distance': 3.3}]



Looking at the `distance_from_selected` it appears that our our trips are still fairly clses to our selected trip.  Notice that most of the data is a distance of .0045 away, so going to the top 7 nearest neighbors didn't seem to give us neighbors too far from each other, which is a good sign.  

Still, it's hard to know what distance in latitude and longitude really look like, so let's map the data. 


```python
midtown_location = location(midtown_trip) # [40.76171, -73.98276]
midtown_map = map_from(midtown_location, 16)
closest_markers = markers_from_trips(seven_closest)

add_markers(closest_markers, midtown_map)
```




<div style="width:100%;"><div style="position:relative;width:100%;height:0;padding-bottom:60%;"><iframe src="data:text/html;charset=utf-8;base64,PCFET0NUWVBFIGh0bWw+CjxoZWFkPiAgICAKICAgIDxtZXRhIGh0dHAtZXF1aXY9ImNvbnRlbnQtdHlwZSIgY29udGVudD0idGV4dC9odG1sOyBjaGFyc2V0PVVURi04IiAvPgogICAgPHNjcmlwdD5MX1BSRUZFUl9DQU5WQVMgPSBmYWxzZTsgTF9OT19UT1VDSCA9IGZhbHNlOyBMX0RJU0FCTEVfM0QgPSBmYWxzZTs8L3NjcmlwdD4KICAgIDxzY3JpcHQgc3JjPSJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvbnBtL2xlYWZsZXRAMS4yLjAvZGlzdC9sZWFmbGV0LmpzIj48L3NjcmlwdD4KICAgIDxzY3JpcHQgc3JjPSJodHRwczovL2FqYXguZ29vZ2xlYXBpcy5jb20vYWpheC9saWJzL2pxdWVyeS8xLjExLjEvanF1ZXJ5Lm1pbi5qcyI+PC9zY3JpcHQ+CiAgICA8c2NyaXB0IHNyYz0iaHR0cHM6Ly9tYXhjZG4uYm9vdHN0cmFwY2RuLmNvbS9ib290c3RyYXAvMy4yLjAvanMvYm9vdHN0cmFwLm1pbi5qcyI+PC9zY3JpcHQ+CiAgICA8c2NyaXB0IHNyYz0iaHR0cHM6Ly9jZG5qcy5jbG91ZGZsYXJlLmNvbS9hamF4L2xpYnMvTGVhZmxldC5hd2Vzb21lLW1hcmtlcnMvMi4wLjIvbGVhZmxldC5hd2Vzb21lLW1hcmtlcnMuanMiPjwvc2NyaXB0PgogICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvbnBtL2xlYWZsZXRAMS4yLjAvZGlzdC9sZWFmbGV0LmNzcyIgLz4KICAgIDxsaW5rIHJlbD0ic3R5bGVzaGVldCIgaHJlZj0iaHR0cHM6Ly9tYXhjZG4uYm9vdHN0cmFwY2RuLmNvbS9ib290c3RyYXAvMy4yLjAvY3NzL2Jvb3RzdHJhcC5taW4uY3NzIiAvPgogICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJodHRwczovL21heGNkbi5ib290c3RyYXBjZG4uY29tL2Jvb3RzdHJhcC8zLjIuMC9jc3MvYm9vdHN0cmFwLXRoZW1lLm1pbi5jc3MiIC8+CiAgICA8bGluayByZWw9InN0eWxlc2hlZXQiIGhyZWY9Imh0dHBzOi8vbWF4Y2RuLmJvb3RzdHJhcGNkbi5jb20vZm9udC1hd2Vzb21lLzQuNi4zL2Nzcy9mb250LWF3ZXNvbWUubWluLmNzcyIgLz4KICAgIDxsaW5rIHJlbD0ic3R5bGVzaGVldCIgaHJlZj0iaHR0cHM6Ly9jZG5qcy5jbG91ZGZsYXJlLmNvbS9hamF4L2xpYnMvTGVhZmxldC5hd2Vzb21lLW1hcmtlcnMvMi4wLjIvbGVhZmxldC5hd2Vzb21lLW1hcmtlcnMuY3NzIiAvPgogICAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJodHRwczovL3Jhd2dpdC5jb20vcHl0aG9uLXZpc3VhbGl6YXRpb24vZm9saXVtL21hc3Rlci9mb2xpdW0vdGVtcGxhdGVzL2xlYWZsZXQuYXdlc29tZS5yb3RhdGUuY3NzIiAvPgogICAgPHN0eWxlPmh0bWwsIGJvZHkge3dpZHRoOiAxMDAlO2hlaWdodDogMTAwJTttYXJnaW46IDA7cGFkZGluZzogMDt9PC9zdHlsZT4KICAgIDxzdHlsZT4jbWFwIHtwb3NpdGlvbjphYnNvbHV0ZTt0b3A6MDtib3R0b206MDtyaWdodDowO2xlZnQ6MDt9PC9zdHlsZT4KICAgIAogICAgICAgICAgICA8c3R5bGU+ICNtYXBfOTM5NmNjOWExZjdkNGFhNjk4MTZkNGQzOTQxZDE4ZWEgewogICAgICAgICAgICAgICAgcG9zaXRpb24gOiByZWxhdGl2ZTsKICAgICAgICAgICAgICAgIHdpZHRoIDogMTAwLjAlOwogICAgICAgICAgICAgICAgaGVpZ2h0OiAxMDAuMCU7CiAgICAgICAgICAgICAgICBsZWZ0OiAwLjAlOwogICAgICAgICAgICAgICAgdG9wOiAwLjAlOwogICAgICAgICAgICAgICAgfQogICAgICAgICAgICA8L3N0eWxlPgogICAgICAgIAo8L2hlYWQ+Cjxib2R5PiAgICAKICAgIAogICAgICAgICAgICA8ZGl2IGNsYXNzPSJmb2xpdW0tbWFwIiBpZD0ibWFwXzkzOTZjYzlhMWY3ZDRhYTY5ODE2ZDRkMzk0MWQxOGVhIiA+PC9kaXY+CiAgICAgICAgCjwvYm9keT4KPHNjcmlwdD4gICAgCiAgICAKCiAgICAgICAgICAgIAogICAgICAgICAgICAgICAgdmFyIGJvdW5kcyA9IG51bGw7CiAgICAgICAgICAgIAoKICAgICAgICAgICAgdmFyIG1hcF85Mzk2Y2M5YTFmN2Q0YWE2OTgxNmQ0ZDM5NDFkMThlYSA9IEwubWFwKAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgJ21hcF85Mzk2Y2M5YTFmN2Q0YWE2OTgxNmQ0ZDM5NDFkMThlYScsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7Y2VudGVyOiBbNDAuNzYxNzEsLTczLjk4Mjc2XSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHpvb206IDE2LAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgbWF4Qm91bmRzOiBib3VuZHMsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBsYXllcnM6IFtdLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgd29ybGRDb3B5SnVtcDogZmFsc2UsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBjcnM6IEwuQ1JTLkVQU0czODU3CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIH0pOwogICAgICAgICAgICAKICAgICAgICAKICAgIAogICAgICAgICAgICB2YXIgdGlsZV9sYXllcl82NThlMTcxODM4ZDc0YzM0YWFkZGFhNWQxMDljYzA0OSA9IEwudGlsZUxheWVyKAogICAgICAgICAgICAgICAgJ2h0dHBzOi8ve3N9LnRpbGUub3BlbnN0cmVldG1hcC5vcmcve3p9L3t4fS97eX0ucG5nJywKICAgICAgICAgICAgICAgIHsKICAiYXR0cmlidXRpb24iOiBudWxsLAogICJkZXRlY3RSZXRpbmEiOiBmYWxzZSwKICAibWF4Wm9vbSI6IDE4LAogICJtaW5ab29tIjogMSwKICAibm9XcmFwIjogZmFsc2UsCiAgInN1YmRvbWFpbnMiOiAiYWJjIgp9CiAgICAgICAgICAgICAgICApLmFkZFRvKG1hcF85Mzk2Y2M5YTFmN2Q0YWE2OTgxNmQ0ZDM5NDFkMThlYSk7CiAgICAgICAgCiAgICAKICAgICAgICAgICAgdmFyIGNpcmNsZV9tYXJrZXJfMTE1YmZiNDM0ZjExNDkzZWIzODVmM2Q0Mjc4NGNhM2QgPSBMLmNpcmNsZU1hcmtlcigKICAgICAgICAgICAgICAgIFs0MC43NjEzNzIsLTczLjk4MjYwMl0sCiAgICAgICAgICAgICAgICB7CiAgImJ1YmJsaW5nTW91c2VFdmVudHMiOiB0cnVlLAogICJjb2xvciI6ICIjMzM4OGZmIiwKICAiZGFzaEFycmF5IjogbnVsbCwKICAiZGFzaE9mZnNldCI6IG51bGwsCiAgImZpbGwiOiBmYWxzZSwKICAiZmlsbENvbG9yIjogIiMzMzg4ZmYiLAogICJmaWxsT3BhY2l0eSI6IDAuMiwKICAiZmlsbFJ1bGUiOiAiZXZlbm9kZCIsCiAgImxpbmVDYXAiOiAicm91bmQiLAogICJsaW5lSm9pbiI6ICJyb3VuZCIsCiAgIm9wYWNpdHkiOiAxLjAsCiAgInJhZGl1cyI6IDYsCiAgInN0cm9rZSI6IHRydWUsCiAgIndlaWdodCI6IDMKfQogICAgICAgICAgICAgICAgKS5hZGRUbyhtYXBfOTM5NmNjOWExZjdkNGFhNjk4MTZkNGQzOTQxZDE4ZWEpOwogICAgICAgICAgICAKICAgIAogICAgICAgICAgICB2YXIgY2lyY2xlX21hcmtlcl9iMzBmMTA5NTdmNDE0YmYyOGU1OTJjNzdiNzc1MGRkNiA9IEwuY2lyY2xlTWFya2VyKAogICAgICAgICAgICAgICAgWzQwLjc2MjQ0NCwtNzMuOTgyNDRdLAogICAgICAgICAgICAgICAgewogICJidWJibGluZ01vdXNlRXZlbnRzIjogdHJ1ZSwKICAiY29sb3IiOiAiIzMzODhmZiIsCiAgImRhc2hBcnJheSI6IG51bGwsCiAgImRhc2hPZmZzZXQiOiBudWxsLAogICJmaWxsIjogZmFsc2UsCiAgImZpbGxDb2xvciI6ICIjMzM4OGZmIiwKICAiZmlsbE9wYWNpdHkiOiAwLjIsCiAgImZpbGxSdWxlIjogImV2ZW5vZGQiLAogICJsaW5lQ2FwIjogInJvdW5kIiwKICAibGluZUpvaW4iOiAicm91bmQiLAogICJvcGFjaXR5IjogMS4wLAogICJyYWRpdXMiOiA2LAogICJzdHJva2UiOiB0cnVlLAogICJ3ZWlnaHQiOiAzCn0KICAgICAgICAgICAgICAgICkuYWRkVG8obWFwXzkzOTZjYzlhMWY3ZDRhYTY5ODE2ZDRkMzk0MWQxOGVhKTsKICAgICAgICAgICAgCiAgICAKICAgICAgICAgICAgdmFyIGNpcmNsZV9tYXJrZXJfZTlhN2ViNzFhNmIzNDgyZGI3OTI3YmE0NDNjNTE4MzAgPSBMLmNpcmNsZU1hcmtlcigKICAgICAgICAgICAgICAgIFs0MC43NjI3NjcsLTczLjk4MjI5M10sCiAgICAgICAgICAgICAgICB7CiAgImJ1YmJsaW5nTW91c2VFdmVudHMiOiB0cnVlLAogICJjb2xvciI6ICIjMzM4OGZmIiwKICAiZGFzaEFycmF5IjogbnVsbCwKICAiZGFzaE9mZnNldCI6IG51bGwsCiAgImZpbGwiOiBmYWxzZSwKICAiZmlsbENvbG9yIjogIiMzMzg4ZmYiLAogICJmaWxsT3BhY2l0eSI6IDAuMiwKICAiZmlsbFJ1bGUiOiAiZXZlbm9kZCIsCiAgImxpbmVDYXAiOiAicm91bmQiLAogICJsaW5lSm9pbiI6ICJyb3VuZCIsCiAgIm9wYWNpdHkiOiAxLjAsCiAgInJhZGl1cyI6IDYsCiAgInN0cm9rZSI6IHRydWUsCiAgIndlaWdodCI6IDMKfQogICAgICAgICAgICAgICAgKS5hZGRUbyhtYXBfOTM5NmNjOWExZjdkNGFhNjk4MTZkNGQzOTQxZDE4ZWEpOwogICAgICAgICAgICAKICAgIAogICAgICAgICAgICB2YXIgY2lyY2xlX21hcmtlcl85NGM2NjU2NjcxYTY0MzVjOTBmOTcxZDAxOThmNDU0ZSA9IEwuY2lyY2xlTWFya2VyKAogICAgICAgICAgICAgICAgWzQwLjc2Mjg2OCwtNzMuOTgzMjMzXSwKICAgICAgICAgICAgICAgIHsKICAiYnViYmxpbmdNb3VzZUV2ZW50cyI6IHRydWUsCiAgImNvbG9yIjogIiMzMzg4ZmYiLAogICJkYXNoQXJyYXkiOiBudWxsLAogICJkYXNoT2Zmc2V0IjogbnVsbCwKICAiZmlsbCI6IGZhbHNlLAogICJmaWxsQ29sb3IiOiAiIzMzODhmZiIsCiAgImZpbGxPcGFjaXR5IjogMC4yLAogICJmaWxsUnVsZSI6ICJldmVub2RkIiwKICAibGluZUNhcCI6ICJyb3VuZCIsCiAgImxpbmVKb2luIjogInJvdW5kIiwKICAib3BhY2l0eSI6IDEuMCwKICAicmFkaXVzIjogNiwKICAic3Ryb2tlIjogdHJ1ZSwKICAid2VpZ2h0IjogMwp9CiAgICAgICAgICAgICAgICApLmFkZFRvKG1hcF85Mzk2Y2M5YTFmN2Q0YWE2OTgxNmQ0ZDM5NDFkMThlYSk7CiAgICAgICAgICAgIAogICAgCiAgICAgICAgICAgIHZhciBjaXJjbGVfbWFya2VyX2VhZmJmOGIyZmJjODRmYmI5NTk5YTEzMThiMGMxNmJmID0gTC5jaXJjbGVNYXJrZXIoCiAgICAgICAgICAgICAgICBbNDAuNzYwMDU3LC03My45ODM1MDJdLAogICAgICAgICAgICAgICAgewogICJidWJibGluZ01vdXNlRXZlbnRzIjogdHJ1ZSwKICAiY29sb3IiOiAiIzMzODhmZiIsCiAgImRhc2hBcnJheSI6IG51bGwsCiAgImRhc2hPZmZzZXQiOiBudWxsLAogICJmaWxsIjogZmFsc2UsCiAgImZpbGxDb2xvciI6ICIjMzM4OGZmIiwKICAiZmlsbE9wYWNpdHkiOiAwLjIsCiAgImZpbGxSdWxlIjogImV2ZW5vZGQiLAogICJsaW5lQ2FwIjogInJvdW5kIiwKICAibGluZUpvaW4iOiAicm91bmQiLAogICJvcGFjaXR5IjogMS4wLAogICJyYWRpdXMiOiA2LAogICJzdHJva2UiOiB0cnVlLAogICJ3ZWlnaHQiOiAzCn0KICAgICAgICAgICAgICAgICkuYWRkVG8obWFwXzkzOTZjYzlhMWY3ZDRhYTY5ODE2ZDRkMzk0MWQxOGVhKTsKICAgICAgICAgICAgCiAgICAKICAgICAgICAgICAgdmFyIGNpcmNsZV9tYXJrZXJfMWFhNGU5M2QzZDJiNDc3YzllMTAxMjM0MjM3MjYwYzYgPSBMLmNpcmNsZU1hcmtlcigKICAgICAgICAgICAgICAgIFs0MC43NjA2NDQsLTczLjk4NDUzMV0sCiAgICAgICAgICAgICAgICB7CiAgImJ1YmJsaW5nTW91c2VFdmVudHMiOiB0cnVlLAogICJjb2xvciI6ICIjMzM4OGZmIiwKICAiZGFzaEFycmF5IjogbnVsbCwKICAiZGFzaE9mZnNldCI6IG51bGwsCiAgImZpbGwiOiBmYWxzZSwKICAiZmlsbENvbG9yIjogIiMzMzg4ZmYiLAogICJmaWxsT3BhY2l0eSI6IDAuMiwKICAiZmlsbFJ1bGUiOiAiZXZlbm9kZCIsCiAgImxpbmVDYXAiOiAicm91bmQiLAogICJsaW5lSm9pbiI6ICJyb3VuZCIsCiAgIm9wYWNpdHkiOiAxLjAsCiAgInJhZGl1cyI6IDYsCiAgInN0cm9rZSI6IHRydWUsCiAgIndlaWdodCI6IDMKfQogICAgICAgICAgICAgICAgKS5hZGRUbyhtYXBfOTM5NmNjOWExZjdkNGFhNjk4MTZkNGQzOTQxZDE4ZWEpOwogICAgICAgICAgICAKICAgIAogICAgICAgICAgICB2YXIgY2lyY2xlX21hcmtlcl8wYTI0ZmMwOTVhYTg0MWZjOWYzMWNhYTNkYTk4YmFjMSA9IEwuY2lyY2xlTWFya2VyKAogICAgICAgICAgICAgICAgWzQwLjc2MjEwNywtNzMuOTg0NzldLAogICAgICAgICAgICAgICAgewogICJidWJibGluZ01vdXNlRXZlbnRzIjogdHJ1ZSwKICAiY29sb3IiOiAiIzMzODhmZiIsCiAgImRhc2hBcnJheSI6IG51bGwsCiAgImRhc2hPZmZzZXQiOiBudWxsLAogICJmaWxsIjogZmFsc2UsCiAgImZpbGxDb2xvciI6ICIjMzM4OGZmIiwKICAiZmlsbE9wYWNpdHkiOiAwLjIsCiAgImZpbGxSdWxlIjogImV2ZW5vZGQiLAogICJsaW5lQ2FwIjogInJvdW5kIiwKICAibGluZUpvaW4iOiAicm91bmQiLAogICJvcGFjaXR5IjogMS4wLAogICJyYWRpdXMiOiA2LAogICJzdHJva2UiOiB0cnVlLAogICJ3ZWlnaHQiOiAzCn0KICAgICAgICAgICAgICAgICkuYWRkVG8obWFwXzkzOTZjYzlhMWY3ZDRhYTY5ODE2ZDRkMzk0MWQxOGVhKTsKICAgICAgICAgICAgCiAgICAKICAgICAgICAgICAgdmFyIGNpcmNsZV9tYXJrZXJfM2M0MDdlOWEwZWFiNDg5MmJiNTdkZDI3NDhiNDM2ODEgPSBMLmNpcmNsZU1hcmtlcigKICAgICAgICAgICAgICAgIFs0MC43NjA0NDIsLTczLjk4MDY0OF0sCiAgICAgICAgICAgICAgICB7CiAgImJ1YmJsaW5nTW91c2VFdmVudHMiOiB0cnVlLAogICJjb2xvciI6ICIjMzM4OGZmIiwKICAiZGFzaEFycmF5IjogbnVsbCwKICAiZGFzaE9mZnNldCI6IG51bGwsCiAgImZpbGwiOiBmYWxzZSwKICAiZmlsbENvbG9yIjogIiMzMzg4ZmYiLAogICJmaWxsT3BhY2l0eSI6IDAuMiwKICAiZmlsbFJ1bGUiOiAiZXZlbm9kZCIsCiAgImxpbmVDYXAiOiAicm91bmQiLAogICJsaW5lSm9pbiI6ICJyb3VuZCIsCiAgIm9wYWNpdHkiOiAxLjAsCiAgInJhZGl1cyI6IDYsCiAgInN0cm9rZSI6IHRydWUsCiAgIndlaWdodCI6IDMKfQogICAgICAgICAgICAgICAgKS5hZGRUbyhtYXBfOTM5NmNjOWExZjdkNGFhNjk4MTZkNGQzOTQxZDE4ZWEpOwogICAgICAgICAgICAKICAgIAogICAgICAgICAgICB2YXIgY2lyY2xlX21hcmtlcl8xZDJjNzA2NjVmY2M0MDk3YjM3MDMzNzUyZmVkMTUzZCA9IEwuY2lyY2xlTWFya2VyKAogICAgICAgICAgICAgICAgWzQwLjc2MzY4NCwtNzMuOTgxMjE0XSwKICAgICAgICAgICAgICAgIHsKICAiYnViYmxpbmdNb3VzZUV2ZW50cyI6IHRydWUsCiAgImNvbG9yIjogIiMzMzg4ZmYiLAogICJkYXNoQXJyYXkiOiBudWxsLAogICJkYXNoT2Zmc2V0IjogbnVsbCwKICAiZmlsbCI6IGZhbHNlLAogICJmaWxsQ29sb3IiOiAiIzMzODhmZiIsCiAgImZpbGxPcGFjaXR5IjogMC4yLAogICJmaWxsUnVsZSI6ICJldmVub2RkIiwKICAibGluZUNhcCI6ICJyb3VuZCIsCiAgImxpbmVKb2luIjogInJvdW5kIiwKICAib3BhY2l0eSI6IDEuMCwKICAicmFkaXVzIjogNiwKICAic3Ryb2tlIjogdHJ1ZSwKICAid2VpZ2h0IjogMwp9CiAgICAgICAgICAgICAgICApLmFkZFRvKG1hcF85Mzk2Y2M5YTFmN2Q0YWE2OTgxNmQ0ZDM5NDFkMThlYSk7CiAgICAgICAgICAgIAogICAgCiAgICAgICAgICAgIHZhciBjaXJjbGVfbWFya2VyX2RiMTY3MzQ5NDg2ZjQwYWFhMTZiMzU4ZWI3MzIwNzE5ID0gTC5jaXJjbGVNYXJrZXIoCiAgICAgICAgICAgICAgICBbNDAuNzU5NjYzLC03My45ODExNDFdLAogICAgICAgICAgICAgICAgewogICJidWJibGluZ01vdXNlRXZlbnRzIjogdHJ1ZSwKICAiY29sb3IiOiAiIzMzODhmZiIsCiAgImRhc2hBcnJheSI6IG51bGwsCiAgImRhc2hPZmZzZXQiOiBudWxsLAogICJmaWxsIjogZmFsc2UsCiAgImZpbGxDb2xvciI6ICIjMzM4OGZmIiwKICAiZmlsbE9wYWNpdHkiOiAwLjIsCiAgImZpbGxSdWxlIjogImV2ZW5vZGQiLAogICJsaW5lQ2FwIjogInJvdW5kIiwKICAibGluZUpvaW4iOiAicm91bmQiLAogICJvcGFjaXR5IjogMS4wLAogICJyYWRpdXMiOiA2LAogICJzdHJva2UiOiB0cnVlLAogICJ3ZWlnaHQiOiAzCn0KICAgICAgICAgICAgICAgICkuYWRkVG8obWFwXzkzOTZjYzlhMWY3ZDRhYTY5ODE2ZDRkMzk0MWQxOGVhKTsKICAgICAgICAgICAgCiAgICAKICAgICAgICAgICAgdmFyIGNpcmNsZV9tYXJrZXJfZjY4OWVlZmY2NzNkNGMzYmIyYzBmMDkxYjA3NTcwMzMgPSBMLmNpcmNsZU1hcmtlcigKICAgICAgICAgICAgICAgIFs0MC43NTkzNDcsLTczLjk4MTUyMl0sCiAgICAgICAgICAgICAgICB7CiAgImJ1YmJsaW5nTW91c2VFdmVudHMiOiB0cnVlLAogICJjb2xvciI6ICIjMzM4OGZmIiwKICAiZGFzaEFycmF5IjogbnVsbCwKICAiZGFzaE9mZnNldCI6IG51bGwsCiAgImZpbGwiOiBmYWxzZSwKICAiZmlsbENvbG9yIjogIiMzMzg4ZmYiLAogICJmaWxsT3BhY2l0eSI6IDAuMiwKICAiZmlsbFJ1bGUiOiAiZXZlbm9kZCIsCiAgImxpbmVDYXAiOiAicm91bmQiLAogICJsaW5lSm9pbiI6ICJyb3VuZCIsCiAgIm9wYWNpdHkiOiAxLjAsCiAgInJhZGl1cyI6IDYsCiAgInN0cm9rZSI6IHRydWUsCiAgIndlaWdodCI6IDMKfQogICAgICAgICAgICAgICAgKS5hZGRUbyhtYXBfOTM5NmNjOWExZjdkNGFhNjk4MTZkNGQzOTQxZDE4ZWEpOwogICAgICAgICAgICAKICAgIAogICAgICAgICAgICB2YXIgY2lyY2xlX21hcmtlcl9lYzFjZjNlMjJiMzM0NDVmODNjN2JhNjY2NGQzNjhiZSA9IEwuY2lyY2xlTWFya2VyKAogICAgICAgICAgICAgICAgWzQwLjc1OTA2LC03My45ODM2ODFdLAogICAgICAgICAgICAgICAgewogICJidWJibGluZ01vdXNlRXZlbnRzIjogdHJ1ZSwKICAiY29sb3IiOiAiIzMzODhmZiIsCiAgImRhc2hBcnJheSI6IG51bGwsCiAgImRhc2hPZmZzZXQiOiBudWxsLAogICJmaWxsIjogZmFsc2UsCiAgImZpbGxDb2xvciI6ICIjMzM4OGZmIiwKICAiZmlsbE9wYWNpdHkiOiAwLjIsCiAgImZpbGxSdWxlIjogImV2ZW5vZGQiLAogICJsaW5lQ2FwIjogInJvdW5kIiwKICAibGluZUpvaW4iOiAicm91bmQiLAogICJvcGFjaXR5IjogMS4wLAogICJyYWRpdXMiOiA2LAogICJzdHJva2UiOiB0cnVlLAogICJ3ZWlnaHQiOiAzCn0KICAgICAgICAgICAgICAgICkuYWRkVG8obWFwXzkzOTZjYzlhMWY3ZDRhYTY5ODE2ZDRkMzk0MWQxOGVhKTsKICAgICAgICAgICAgCjwvc2NyaXB0Pg==" style="position:absolute;width:100%;height:100%;left:0;top:0;border:none !important;" allowfullscreen webkitallowfullscreen mozallowfullscreen></iframe></div></div>



Ok.  These locations stay fairly close to our estimated location of 51st street and 7th Avenue.  So they could be a good estimate of a trip distance.


```python
median_distance(seven_closest)
```




    1.91



Ok, now let's try a different location


```python
charging_bull_closest = nearest_neighbors({'pickup_latitude': 40.7049, 'pickup_longitude': -74.0137}, cleaned_trips, number = 12)
```


```python
median_distance(charging_bull_closest) # 3.515
```




    3.515



Ok, so there appears to be a significant difference between choosing a location around 51st street versus choosing a location at Wall Street.  

### Summary

Ok, so in this lab, we used the nearest neighbors function to predict the length of a taxi ride.  To do so, we selected a location, then found a number of closest taxi rides to that location, and then took the median trip lengths of the nearest neighbors to find an estimate of the new ride's trip length.  You can see that even with just a little bit of math and programming we can begin to make meaningful predictions with data.
