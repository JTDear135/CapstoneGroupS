# type: ignore
from typing import Tuple, List
import pandas as pd
from geopy import Point
from collections import defaultdict
from geopy.distance import geodesic
from geographiclib.geodesic import Geodesic
# to visualize
import folium
'''
Flight Path Component.

This script calculates waypoints between two airports based on their ICAO/IATA codes.

Features:
    - Reads airport data from a CSV file. (This will need to be changed when merging with the driver!!!!)
    - Retrieves coordinates for given airport codes. (Private)
    - Computes equally spaced waypoints along a great-circle path. (We can choose how may points along the path we want)
    - Uses GeographicLib for precise bearing calculations. (precise just means not in a straight line. Instead, this library takes into consideration the curvature of the earth!)

'''

class FlightPath:

    airport_data =pd.read_csv("../airport_info/airports_data.csv")

    def __init__(self, departure_code: str, destination_code: str):
        self.departure = self.__get_coordinates(departure_code)
        self.destination = self.__get_coordinates(destination_code)
        pass
    

    def __get_coordinates(self, airport_code):
        """
        Translates Airport Codes to Coordinates.

        Args:
            airport_code (str): Aiport Code (for now it is accepting both ICAC and IATA format)
    
        Returns:
            (latitude, longitude) tuple(str): Tuple of latitude and longitude of the airport position
        """
        row = self.airport_data.loc[(self.airport_data["ICAO"] == airport_code) | (self.airport_data["IATA"] == airport_code)] # This can be changed to only ICAC in the future when merging.

        if row.empty:
            raise ValueError(f"Airport code {airport_code} not found in the dataset.")
        
        latitude = row.iloc[0]["Latitude"]
        longitude = row.iloc[0]["Longitude"]

        return latitude, longitude
    
    
    def get_waypoints(self, n: int) -> List[Tuple[float, float]]:
        """
        Generates `n` waypoints along the flight path.

        Uses the great-circle distance to compute equally spaced waypoints from 
        the departure airport to the destination.

        Args:
            n (int): Number of waypoints to generate.

        Returns:
            list: A list of tuples containing the latitude and longitude of each waypoint, including the departure and destination airport
        """
        # turn the coords into points using geopy library
        depart = Point(self.departure[0], self.departure[1])
        dest = Point(self.destination[0], self.destination[1])
        result = [(depart.latitude, depart.longitude)]
        
        # when dest == depart, we return the coordinates of the departure airport
        if (depart == dest):
            return result
        
        # find n points on the way
        total_dist = geodesic(depart, dest).km # this is real world distance on earth, great-circle distance.
        step_size = total_dist/ (n+1)
        # get the direction of the two points, bearing (angle of the line)
        bearing = Geodesic.WGS84.Inverse(self.departure[0], self.departure[1], self.destination[0], self.destination[1])

        for i in range(1, n+1):
            next_point = geodesic(kilometers = step_size * i).destination(depart, bearing["azi1"]) # --> az1 here is the initial bearing (the angle of the line from the departure to the destination airport)
            result.append((next_point.latitude, next_point.longitude))
        
        result.append((dest.latitude, dest.longitude))
        
        return result

# for testing purposes only!
def main():
    departure = input("Enter Departure Airport\n")
    destination = input("Enter Destination Airport\n")

    flight_path = FlightPath(departure, destination)

    num_points = input("How many waypoints\n")
    waypoints = flight_path.get_waypoints(int(num_points)) # you can choose how many points you want between the depart and destination here.

    # to visualize
    m = folium.Map(location=waypoints[0], zoom_start=5)

    # Add pins for each coordinate on the map
    for coord in waypoints:
        folium.Marker(coord).add_to(m)

    m.save("map.html")
    print("Map saved")

if __name__ == "__main__":
    main()
