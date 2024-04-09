__ASSIGNMENT-2__

NAME : VAIDEHI SUDELE

HOW TO RUN THE CODE : Use command : pipenv run python assignment2.py --urls files.csv

BUGS AND ASSUMPTIONS :

Assuming that the format of the date and time stays the same
Presumptively every PDF's data will be downloaded before being processed
Assumed using the Google Maps API, which requires an API key, is appropriate
There is a daily limit of 2500 free requests for Google API.

IMPORTANT FUNCTIONS :

Certainly! Here are the descriptions for all the functions in the provided code:

1. **fetch_incidents(url)**
   - Description: Fetches incident data from the provided URL(s) by making an HTTP request and reading the response.
   - Parameters:
     - `url`: String containing the URL from which incident data needs to be fetched.
   - Returns:
     - Data fetched from the URL.

2. **extract_incidents(f_data)**
   - Description: Extracts incident records from the fetched PDF data by parsing the text content.
   - Parameters:
     - `f_data`: Byte data representing the content of the fetched PDF file.
   - Returns:
     - List of dictionaries containing extracted incident records.

3. **split_record_components(incident)**
   - Description: Splits the components of an incident record into date, time, incident number, middle components, and origin.
   - Parameters:
     - `incident`: String representing a single incident record.
   - Returns:
     - Tuple containing date, time, incident number, middle components, and origin.

4. **adjust_incident_number(inc_num, middle)**
   - Description: Adjusts the incident number if it exceeds 13 characters.
   - Parameters:
     - `inc_num`: String representing the incident number.
     - `middle`: List of middle components of the incident record.
   - Returns:
     - Tuple containing adjusted incident number and middle components.

5. **is_location_component(component)**
   - Description: Checks if a component is likely to be part of the location in an incident record.
   - Parameters:
     - `component`: String representing a component of the incident record.
   - Returns:
     - Boolean indicating whether the component is likely part of the location.

6. **process_middle_components(middle)**
   - Description: Processes middle components of an incident record to separate location and nature.
   - Parameters:
     - `middle`: List of middle components of the incident record.
   - Returns:
     - Tuple containing lists of location and nature components.

7. **handle_numeric_edge_case_in_location(loc, nat)**
   - Description: Handles a specific edge case in location components where numeric components are encountered.
   - Parameters:
     - `loc`: List of location components.
     - `nat`: List of nature components.
   - Returns:
     - Tuple containing updated lists of location and nature components.

8. **create_inc_record(date, time, inc_num, loc, nat, ori)**
   - Description: Creates an incident record dictionary with provided attributes.
   - Parameters:
     - `date`: Date of the incident.
     - `time`: Time of the incident.
     - `inc_num`: Incident number.
     - `loc`: Location of the incident.
     - `nat`: Nature of the incident.
     - `ori`: Origin of the incident.
   - Returns:
     - Dictionary representing the incident record.

9. **get_inc_details(pg_con)**
   - Description: Extracts details of incident records from page content.
   - Parameters:
     - `pg_con`: List of strings representing incident records on a page.
   - Returns:
     - List of dictionaries containing details of incident records.

10. **calculate_day_time(incident)**
    - Description: Calculates the day of the week and time of day for an incident based on its timestamp.
    - Parameters:
      - `incident`: Dictionary representing the incident record.
    - Returns:
      - Updated incident record dictionary with day of the week and time of day added.

11. **calculate_incident_rank(inc_records)**
    - Description: Calculates the rank of each incident based on its frequency.
    - Parameters:
      - `inc_records`: List of dictionaries representing incident records.
    - Returns:
      - Updated list of incident records with incident rank added.

12. **calculate_location_rank(inc_records)**
    - Description: Calculates the rank of each incident location based on its frequency.
    - Parameters:
      - `inc_records`: List of dictionaries representing incident records.
    - Returns:
      - Updated list of incident records with location rank added.

13. **calculate_emsstatl(inc_records)**
    - Description: Determines if an incident is EMSSTATL (Emergency Medical Services Status at Location).
    - Parameters:
      - `inc_records`: List of dictionaries representing incident records.
    - Returns:
      - Updated list of incident records with EMSSTATL status added.

14. **determine_side_of_town(lat, lng)**
    - Description: Determines the side of town based on latitude and longitude coordinates.
    - Parameters:
      - `lat`: Latitude coordinate.
      - `lng`: Longitude coordinate.
    - Returns:
      - String representing the side of town.

15. **fetch_weather(lat, lng, timestamp)**
    - Description: Fetches weather information using open-meteo API based on latitude, longitude, and timestamp.
    - Parameters:
      - `lat`: Latitude coordinate.
      - `lng`: Longitude coordinate.
      - `timestamp`: Timestamp of the incident.
    - Returns:
      - Weather information.

16. **main(url_file)**
    - Description: Main function to orchestrate the fetching, extraction, analysis, and output of incident data.
    - Parameters:
      - `url_file`: Path to the text file containing URLs of incident summary PDF files.

These are the descriptions for all the functions in the provided code.

