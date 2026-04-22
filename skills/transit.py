import requests
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TRANSITLAND_API_KEY")
BASE = "https://transit.land/api/v2/rest"

geolocator = Nominatim(user_agent="transit_app")

def time_until(target_time_str):
    now = datetime.now()

    # parse input like "20:54:12"
    target_time = datetime.strptime(target_time_str, "%H:%M:%S").time()

    target = datetime.combine(now.date(), target_time)

    # if it's already passed today, roll to next day
    if target < now:
        target += timedelta(days=1)

    delta = target - now
    total_minutes = int(delta.total_seconds() // 60)

    hours = total_minutes // 60
    minutes = total_minutes % 60

    if hours == 0:
        return f"{minutes} min"
    elif minutes == 0:
        return f"{hours} hr"
    else:
        return f"{hours} hr, {minutes} min"

def resolve_to_latlong(location_input):
    print(location_input)
    # Case 1: Already coordinates (tuple like (lat, lon))
    if isinstance(location_input, tuple) and len(location_input) == 2:
        return location_input

    # Case 2: String (address, postal code, place name)
    if isinstance(location_input, str):
        location = geolocator.geocode(location_input)
        if location:
            return location.latitude, location.longitude

    # If nothing works
    raise ValueError("Invalid location input")

def get_nearby_stops(lat, lon, radius):
    url = f"{BASE}/stops"
    params = {
        "lat": lat,
        "lon": lon,
        "radius": radius,
        "apikey": API_KEY
    }

    r = requests.get(url, params=params)
    return r.json().get("stops", [])


def get_departures(onestop_id):
    url = f"{BASE}/stops/{onestop_id}/departures"

    params = {
        "apikey": API_KEY,
        "limit": 3,
    }

    r = requests.get(url, params=params).json()
    return r

#s-dpz2q2twvb-islingtonaveatvandusenblvd

def build_board(location, radius=400):
    lat, lon = resolve_to_latlong(location)
    stops = get_nearby_stops(lat, lon, radius)

    results = []

    stop_ids = []

    for stop in stops:
        stop_name = stop.get("stop_name", "Unknown Stop")
        onestop_id = stop.get("onestop_id")

        if not onestop_id:
            continue

        if onestop_id in stop_ids:
            continue
        else:
            stop_ids.append(onestop_id)

        departures = get_departures(onestop_id)

        departures_list = []

        departures = dict(departures)

        for departure in departures["stops"][0]["departures"]:
            arrival_time = time_until(departure["arrival_time"])
            route = departure['trip']['route']['route_short_name']
            route_name = departure['trip']['route']['route_long_name']
            headsign = departure['trip']['trip_headsign']

            departures_list.append({"arr_time":arrival_time,"rt_num":route,"rt_name":route_name,"headsign":headsign})
        
        results.append({
            "stop_name": stop_name,
            "onestop_id": onestop_id,
            "departures": departures_list
        })

    return results


if __name__ == "__main__":
    location = "Islington Subway Station"

    data = build_board(location, radius=200)

    for id, stop in enumerate(data):
        print(f"\n🚏 {stop['stop_name']}")
        for departure in data[id]['departures']:
            print(f"{departure["rt_num"]} - {departure["rt_name"]}")
            print(f"{departure["headsign"]}")
            print(f"Arriving In: {departure["arr_time"]}")
            print("")