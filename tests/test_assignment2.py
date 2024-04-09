import pytest
from unittest.mock import Mock, patch
from assignment2 import *

# Test for calculate_day_time function
def test_calculate_day_time():
    incident = {
        "inc_time": "04/01/2024 12:30",
        "inc_number": "ABC123",
        "inc_location": "MVA; INJURY; NE",
        "inc_nature": "MVA",
        "inc_ori": ""
    }
    updated_incident = calculate_day_time(incident)
    assert updated_incident["day_of_week"] == 1  # Assuming April 1, 2024 is a Monday (0-indexed)
    assert updated_incident["time_of_day"] == 12

# Test for extract_nature function
def test_extract_nature():
    record = {
        "inc_time": "04/01/2024 12:30",
        "inc_number": "ABC123",
        "inc_location": "MVA; INJURY; NE",
        "inc_nature": "MVA",
        "inc_ori": ""
    }
    assert extract_nature(record) == "MVA"

# Test for calculate_incident_rank function
def test_calculate_incident_rank():
    inc_records = [
        {"inc_time": "04/01/2024 12:30", "inc_number": "ABC123", "inc_location": "MVA; INJURY; NE", "inc_nature": "MVA", "inc_ori": ""},
        {"inc_time": "04/02/2024 14:45", "inc_number": "XYZ456", "inc_location": "FIRE; RESCUE; NW", "inc_nature": "FIRE", "inc_ori": ""},
        {"inc_time": "04/03/2024 09:15", "inc_number": "DEF789", "inc_location": "THEFT; SUSPECT IN CUSTODY; SE", "inc_nature": "THEFT", "inc_ori": ""},
        {"inc_time": "04/04/2024 18:20", "inc_number": "GHI101", "inc_location": "ASSAULT; NO INJURY; SW", "inc_nature": "ASSAULT", "inc_ori": ""}
    ]
    ranked_inc_records = calculate_incident_rank(inc_records)
    
    # Check if incident ranks are assigned correctly
    assert ranked_inc_records[0]["incident_rank"] == 1
    assert ranked_inc_records[1]["incident_rank"] == 2
    assert ranked_inc_records[2]["incident_rank"] == 3
    assert ranked_inc_records[3]["incident_rank"] == 4


def test_calculate_location_rank():
    inc_records = [
        {"inc_location": "Main Street"},
        {"inc_location": "Broadway"},
        {"inc_location": "Main Street"}
    ]
    result = calculate_location_rank(inc_records)
    assert result[0]["location_rank"] == 1
    assert result[1]["location_rank"] == 2
    assert result[2]["location_rank"] == 1



