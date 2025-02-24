import pytest
from flight_path.flight_path import FlightPath

# Test to check for the return type. It should be a tuple of length 2.
def test_get_coordinates_valid():
    flight_path = FlightPath("JFK", "LAX") # => manualy these are correct ones!
    assert isinstance(flight_path.departure, tuple)
    assert len(flight_path.departure) == 2

# Tests for invalid airports
def test_get_coordinates_invalid():
    """Test if __get_coordinates raises an error for an invalid airport code."""
    with pytest.raises(ValueError):
        FlightPath("INVALID", "LAX")

# Tests the size of the waypoints list is correct.
# Essentially if n is the number of waypoints, the returned list shoudl have n+2
@pytest.mark.parametrize("n", [0, 1, 5, 10, 150, 202, 34468, 4444])
def test_get_waypoints(n):
    flight_path = FlightPath("JFK", "LAX")
    waypoints = flight_path.get_waypoints(n)
    assert len(waypoints) == n + 2 

# Test if waypoints list that is returned is a set of unique coordonates.
def test_waypoints_not_identical():
    flight_path = FlightPath("JFK", "LAX")
    waypoints = flight_path.get_waypoints(5)
    
    unique_waypoints = len(set(waypoints)) 
    assert unique_waypoints == len(waypoints), "Waypoints should be unique"

