import os
import io
import re
import sqlite3
import argparse
import urllib.request
from pypdf import PdfReader
from datetime import datetime
from math import atan2, degrees
import googlemaps
import requests

# Initialize the Google Maps client with your API key
gmaps = googlemaps.Client(key='AIzaSyClZlEtRIaxf3ve6wz40pabZp0D0loMohI')

## Global variable for storing day names
DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


# Delete the existing SQLite database file if it exists
def db_delete():
    db_file = 'normanpd.db'
    try:
        if os.path.exists(f'resources/{db_file}'):
            os.remove(f'resources/{db_file}')
    except Exception as err:
        print("Error: ", err)


# Fetch incident data from the provided URL
def fetch_incidents(url):
    try:
        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (HTML, like Gecko) Chrome/24.0.1312.27 "
                          "Safari/537.17"}
        data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read()
        return data
    except Exception as err:
        print("Error: ", err)

# Extract incident records from the fetched PDF data
def extract_incidents(f_data):
    io_data = io.BytesIO(f_data)
    pdf = PdfReader(io_data)

    inc_rec = []
    # Regex pattern for date (MM/DD/YYYY or M/D/YYYY)
    date_pattern = r'\b(?:0?[1-9]|1[0-2])/(?:0?[1-9]|[12][0-9]|3[01])/(?:20\d{2})\b'

    for i_page in range(len(pdf.pages)):
        page = pdf.pages[i_page]
        page_con = page.extract_text()

        # Adjust the extraction for the first page if necessary
        if i_page == 0:
            page_con = page_con[57:-55]

        # Split the content using the date regex, keeping the dates as part of the result
        ext_cont = re.split(f'({date_pattern})', page_con)

        # Reconstruct the incidents with their dates
        inc_con = []
        for i in range(1, len(ext_cont), 2):
            inc_con.append(ext_cont[i] + ext_cont[i + 1])
        # If it's the last page, remove the last line after splitting by date
        if i_page == len(pdf.pages) - 1:
            inc_con = inc_con[:-1]
        # Extract records from the reconstructed text
        for txt in inc_con:
            inc_record = get_inc_details([txt])
            inc_rec.extend(inc_record)

    return inc_rec


# Split incident record into components
def split_record_components(incident):
    components = incident.split()
    date, time, incident_num, *middle, ori = components
    return date, time, incident_num, middle, ori


# Adjust incident number if it's longer than 13 characters
def adjust_incident_number(inc_num, middle):
    if len(inc_num) > 13:
        return inc_num[:13], [inc_num[13:]] + middle
    return inc_num, middle


# Check if a component is likely to be part of the location
def is_location_component(component):
    return (
            component not in ["MVA", "COP", "EMS", "RAMPMVA"] and
            (component.isdecimal() or component.isupper() or component == "/" or ';' in component or component == '1/2')
    )


# Process middle components of an incident record
def process_middle_components(middle):
    loc, nat = [], []
    for rec in middle:
        if len(nat) == 0 and is_location_component(rec):
            loc.append(rec)
        elif rec in ['HWYMotorist', 'RAMPMotorist']:
            loc.append(rec.split('Motorist')[0])
            nat.append('Motorist')
        elif rec == "RAMPMVA":
            loc.append('RAMP')
            nat.insert(0, 'MVA')
        else:
            nat.append(rec)
    return loc, nat


# Handle a specific edge case in location components
def handle_numeric_edge_case_in_location(loc, nat):
    if loc and loc[-1].isdigit() and len(loc[-1]) != 1:
        nat.insert(0, loc.pop())
    return loc, nat


# Create an incident record dictionary
def create_inc_record(date, time, inc_num, loc, nat, ori):
    incident_time = f"{date} {time}" 
    return {
        "inc_time": incident_time,
        "inc_number": inc_num,
        "inc_location": " ".join(loc),
        "inc_nature": " ".join(nat),
        "inc_ori": ori,
    }


# Get details of incident records
def get_inc_details(pg_con):
    inc_list = []
    for inc in pg_con:
        date, time, inc_num, middle, ori = split_record_components(inc)
        inc_num, middle = adjust_incident_number(inc_num, middle)
        loc, nat = process_middle_components(middle)
        loc, nat = handle_numeric_edge_case_in_location(loc, nat)
        inc_record = create_inc_record(date, time, inc_num, loc, nat, ori)
        inc_list.append(inc_record)
    return inc_list


# Calculate day of week and time of day
def calculate_day_time(incident):
    time_str = incident["inc_time"]
    time_obj = datetime.strptime(time_str, '%m/%d/%Y %H:%M')
    day_of_week = time_obj.weekday() + 1  # Monday is 0, so add 1 to match the required range
    time_of_day = time_obj.hour  # Extract hour
    incident["day_of_week"] = day_of_week
    incident["time_of_day"] = time_of_day
    return incident

# Extract nature of incident from the source record
def extract_nature(record):
    return record["inc_nature"]

# Function to calculate incident rank
def calculate_incident_rank(inc_records):
    incident_count = {}
    for record in inc_records:
        nature = extract_nature(record)
        incident_count[nature] = incident_count.get(nature, 0) + 1

    # Sort the incidents by frequency in descending order
    sorted_incidents = sorted(incident_count.items(), key=lambda x: x[1], reverse=True)

    # Initialize incident rank dictionary
    incident_rank = {nature: rank + 1 for rank, (nature, _) in enumerate(sorted_incidents)}

    # Assign incident rank to each record
    for record in inc_records:
        nature = extract_nature(record)
        record["incident_rank"] = incident_rank[nature]

    return inc_records

# Function to calculate location rank
def calculate_location_rank(inc_records):
    location_count = {}
    for record in inc_records:
        location = record["inc_location"]
        location_count[location] = location_count.get(location, 0) + 1

    # Sort the locations by frequency in descending order
    sorted_locations = sorted(location_count.items(), key=lambda x: x[1], reverse=True)

    # Initialize location rank dictionary
    location_rank = {location: rank + 1 for rank, (location, _) in enumerate(sorted_locations)}

    # Assign location rank to each record
    for record in inc_records:
        location = record["inc_location"]
        record["location_rank"] = location_rank[location]

    return inc_records

# Function to calculate EMSSTATL value
def calculate_emsstatl(inc_records):
    for i, record in enumerate(inc_records):
        ori = record["inc_ori"]
        inc_location = record["inc_location"]
        inc_time = record["inc_time"]

        # Check if the Incident ORI was EMSSTAT
        if ori == "EMSSTAT":
            record["EMSSTATL"] = 1
            continue

        # Check if the subsequent record or two contain an EMSSTAT at the same time and location
        for j in range(i + 1, min(i + 3, len(inc_records))):
            next_record = inc_records[j]
            if next_record["inc_time"] == inc_time and next_record["inc_location"] == inc_location:
                if next_record["inc_ori"] == "EMSSTAT":
                    record["EMSSTATL"] = 1
                    break
        else:
            record["EMSSTATL"] = 0

    return inc_records


# Function to determine the side of town
def determine_side_of_town(lat, lng):
    # Coordinates of the center of town
    center_lat, center_lng = 35.220833, -97.443611

    # Calculate the angle between the center of town and the given coordinates
    angle = degrees(atan2(lat - center_lat, lng - center_lng))

    # Determine the side of town based on the angle
    if angle < 0:
        angle += 360

    side_of_town = None

    if 22.5 <= angle < 67.5:
        side_of_town = 'NE'
    elif 67.5 <= angle < 112.5:
        side_of_town = 'E'
    elif 112.5 <= angle < 157.5:
        side_of_town = 'SE'
    elif 157.5 <= angle < 202.5:
        side_of_town = 'S'
    elif 202.5 <= angle < 247.5:
        side_of_town = 'SW'
    elif 247.5 <= angle < 292.5:
        side_of_town = 'W'
    elif 292.5 <= angle < 337.5:
        side_of_town = 'NW'
    else:
        side_of_town = 'N'

    return side_of_town


# Function to fetch weather information from open-meteo API
def fetch_weather(lat, lng, timestamp):
    timestamp = datetime.strptime(timestamp, "%m/%d/%Y %H:%M")
    if lat is None or lng is None:
        return "Unknown"
    formatted_date = timestamp.date()
    formatted_hour = timestamp.hour

    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lng,
        "start_date": formatted_date,
        "end_date": formatted_date,
        "hourly": "weather_code"
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            weather = data['hourly']['weather_code'][formatted_hour]
            return weather
    except requests.RequestException as e:
        print(f"Error fetching weather: {e}")
    return None



#all functions are called in main function 
def main(url_file):
    with open(url_file, 'r') as file:
        urls = file.readlines()
        for url in urls:
            url = url.strip()
            if url:
                # Download data
                inc_data = fetch_incidents(url)

                # Extract data
                inc_records = extract_incidents(inc_data)
                inc_records = calculate_incident_rank(inc_records)
                inc_records = calculate_location_rank(inc_records)
                inc_records = calculate_emsstatl(inc_records)
                for record in inc_records:
                    record = calculate_day_time(record)

                    # Initialize latitude and longitude with default values
                    lat, lng = None, None

                    # Use Google Maps Geocoding API to get latitude and longitude of the incident location
                    location = record["inc_location"]
                    if location:
                        try:
                            geocode_result = gmaps.geocode(location)
                        except googlemaps.exceptions.ApiError as e:
                            print(f"Error geocoding location '{location}': {e}")
                            continue

                        # If geocoding is successful, determine the side of town and add it to the record
                        if geocode_result:
                            lat = geocode_result[0]['geometry']['location']['lat']
                            lng = geocode_result[0]['geometry']['location']['lng']
                            side_of_town = determine_side_of_town(lat, lng)
                            record["side_of_town"] = side_of_town
                        else:
                            record["side_of_town"] = "Unknown"
                    else:
                        record["side_of_town"] = "Unknown"

                    # Fetch weather information
                    weather_info = fetch_weather(lat, lng, record['inc_time'])
                    record['weather'] = weather_info

                
                    emsstatl = 1 if record.get("EMSSTATL", 0) else 0
                    print(f"{record['day_of_week']:<5}\t{record['time_of_day']:<5}\t{record['weather']:<5}\t{record['location_rank']:<5}\t{record.get('side_of_town', '')}\t{record['incident_rank']:<5}\t{record['inc_nature']:<30}\t{emsstatl}")
                    #print(f"{record['day_of_week']}\t{record['time_of_day']}\t{record['location_rank']}\t{record['incident_rank']}\t{record['inc_nature']}\t{emsstatl}")
                    
            


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls", type=str, required=True, help="File containing list of incident summary URLs.")
    args = parser.parse_args()
    if args.urls:
        main(args.urls)

