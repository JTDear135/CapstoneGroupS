from dataclasses import dataclass
from typing import Any
import requests

from pydantic import ValidationError

from .exceptions import (
    NotamFetcherRequestError,
    NotamFetcherUnauthenticatedError,
    NotamFetcherUnexpectedError,
    NotamFetcherValidationError,
)


from .api_schema import Notam, NotamAPIResponse, NotamApiItem 


class NotamRequest:
    page_num: int = 1
    page_size: int = 1000

@dataclass
class NotamLatLongRequest(NotamRequest):
    lat: float
    long: float
    radius: float

@dataclass
class NotamAirportCodeRequest(NotamRequest):
    airport_code: str

class NotamFetcher:
    FAA_API_URL = "https://external-api.faa.gov/notamapi/v1/notams"

    def __init__(self, client_id: str, client_secret: str, page_size: int = 1000):
        self.client_id = client_id
        self.client_secret = client_secret

        if page_size > 1000:
            raise ValueError("page_size must be less than 1000")
    
        self._page_size = page_size

    
    def fetch_notams_by_airport_code(self, airport_code: str):
        """
        Fetches ALL notams for a particular latitude and longitude.

        Args:
            airport_code (str): A valid airport code.

        Raises:
            NotamFetcherRequestError: If a request error occurs while fetching from the API.
            NotamFetcherUnexpectedError: If an unexpected error occurs.
        Returns:
            Notams (List[Notam]): A list of NOTAMs
        """
        request = NotamAirportCodeRequest(airport_code)
        request.page_size = self._page_size

        return self._fetch_all_notams(request)

    def fetch_notams_by_latlong(self, lat: float, long: float, radius: float = 100.0):
        """
        Fetches ALL notams for a particular latitude and longitude.

        Args:
            lat (float): The latitude to fetch NOTAMs from
            long (float): The longitude to fetch NOTAMs from
            radius (float): The location radius criteria in nautical miles. (max:100)

        Raises:
            NotamFetcherRequestError: If a request error occurs while fetching from the API.
            NotamFetcherUnexpectedError: If an unexpected error occurs.
        Returns:
            Notams (List[Notam]): A list of NOTAMs
        """
        if radius > 100:
            raise ValueError(f"Radius must be less than 100")
        if radius <= 0:
            raise ValueError(f"Radius must be greater than 0")
        
        request = NotamLatLongRequest(lat, long, radius)
        request.page_size = self._page_size

        return self._fetch_all_notams(request)

    def _fetch_all_notams(self, request: NotamAirportCodeRequest | NotamLatLongRequest) -> list[Notam]:
        """
        Fetches NOTAMs from all pages of the API
        """
        
        notamItems: list[Notam] = []

        first_page = self._fetch_notams(request)

        notamItems.extend(
            [
                item.properties.coreNOTAMData.notam
                for item in first_page.items
                if isinstance(item, NotamApiItem)
            ]
        )

        for i in range(2, first_page.total_pages + 1):
            request.page_num = i
            nextPage = self._fetch_notams(request)
            notamItems.extend(
                [
                    item.properties.coreNOTAMData.notam
                    for item in nextPage.items
                    if isinstance(item, NotamApiItem)
                ]
            )
        
        return notamItems




 
        


    def _fetch_notams(self, request: NotamAirportCodeRequest | NotamLatLongRequest) -> NotamAPIResponse:
        """
        Fetches and validates a response from the API.

        Args:


        Returns:
            NotamAPIResponse: A Notam API Response

        Raises:
            NotamFetcherRequestError: If a request error occurs while fetching from the API.
            NotamFetcherUnexpectedError: If an unexpected error occurs.
            ValueError: If the request is invalid.
        """
        if request.page_num < 1:
            raise ValueError("page_num must be greater than 0")

        json = self._fetch_notams_raw(request)
        try:
            valid_response = NotamAPIResponse.model_validate(json)
            return valid_response
        except ValidationError:
            raise (
                NotamFetcherValidationError(
                    f"Could not validate response from API.", json
                )
            )
        
    def _fetch_notams_raw(self, request: NotamAirportCodeRequest | NotamLatLongRequest) -> dict[str, Any]:
        
        query_string ={}

        if isinstance(request, NotamLatLongRequest):
            if request.radius > 100:
                raise ValueError("radius must be less than 100")
            if request.radius <= 0:
                raise ValueError("radius must be greater than 0")

            query_string = {
                "locationLongitude": str(request.long),
                "locationLatitude": str(request.lat),
                "locationRadius": str(request.radius),
                "page_num": str(request.page_num),
                "page_size": str(request.page_size),
            }

        if isinstance(request, NotamAirportCodeRequest):
            query_string = {
                "domesticLocation": str(request.airport_code),
                "page_num": str(request.page_num),
                "page_size": str(request.page_size),
            }


        try:
            response = requests.get(
                self.FAA_API_URL,
                headers={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
                params=query_string,
            )
        except requests.exceptions.RequestException as e:
            raise NotamFetcherRequestError from e

        try:
            data = response.json()
            if data.get("error", "") == "Invalid client id or secret":
                raise (NotamFetcherUnauthenticatedError("Invalid client id or secret"))
            
            return data
        except requests.exceptions.JSONDecodeError:
            raise (
                NotamFetcherUnexpectedError(
                    f"Response from API unexpectedly not JSON. Received text: {response.text} "
                )
            )
        
