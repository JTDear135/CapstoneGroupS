from pytest import MonkeyPatch
import pytest
import requests
from notam_fetcher.exceptions import NotamFetcherValidationError
from notam_fetcher.notam_fetcher import NotamFetcher

from typing import Any


class MockResponse:
    """
    This class only mocks the .json() of a request.Response.

    Used to test different JSON responses.

    Example:
    monkeypatch.setattr(requests, "get", returnInvalid)

    """
    def __init__(self, response: dict[str, Any]):
        self.response = response

    def json(self) -> dict[str, Any]:
        return self.response


@pytest.fixture
def mock_api_received_invalid_json(monkeypatch: MonkeyPatch):
    def returnInvalid(*args: Any, **kwargs: Any) -> MockResponse:
        return MockResponse(
            {"Invalid": "This object does not match the schema and cannot be validated"}
        )

    monkeypatch.setattr(requests, "get", returnInvalid)



@pytest.fixture
def mock_unexpected_response(monkeypatch: MonkeyPatch):
    def returnUnexpected(*args: Any, **kwargs: Any) -> MockResponse:
        return MockResponse(
            {
                "pageSize": 10,
                "pageNum": 3,
                "totalCount": 124,
                "totalPages": 13,
                "items": [
                    {
                        "type": "Point",
                        "geometry": {"type": "Point", "coordinates": [0]},
                        "properties": {"name": "Dinagat Islands"},
                    }
                ],
            }
        )

    monkeypatch.setattr(requests, "get", returnUnexpected)


@pytest.fixture
def mock_empty_response(monkeypatch: MonkeyPatch):
    def returnEmpty(*args: Any, **kwargs: Any) -> MockResponse:
        return MockResponse(
            {
                "pageSize": 50,
                "pageNum": 1,
                "totalCount": 0,
                "totalPages": 0,
                "items": [],
            }
        )

    monkeypatch.setattr(requests, "get", returnEmpty)


def test_fetch_notams_by_latlong_invalid_json(mock_api_received_invalid_json: None):
    """Test that an invalid schema from the API raises validation error"""
    notam_fetcher = NotamFetcher("CLIENT_ID", "CLIENT_SECRET")

    with pytest.raises(NotamFetcherValidationError) as e:
        notam_fetcher.fetch_notams_by_latlong(32, 32, 10)

    assert (
        e.value.invalid_object.get("Invalid")
        == "This object does not match the schema and cannot be validated"
    )



def test_fetch_notams_by_latlong_unexpected_response(mock_unexpected_response: None):
    """Test that fetch_notams_by_latlong filters a non-notam object in the NOTAMs API response"""
    notam_fetcher = NotamFetcher("CLIENT_ID", "CLIENT_SECRET")
    with pytest.raises(NotamFetcherValidationError):
        notam_fetcher.fetch_notams_by_latlong(32, 32, 10)


def test_fetch_notams_by_latlong_no_notams(mock_empty_response: None):
    """Test that fetch_notams_by_latlong handles the case where API returns no NOTAMs"""
    notam_fetcher = NotamFetcher("CLIENT_ID", "CLIENT_SECRET")
    notams = notam_fetcher.fetch_notams_by_latlong(32, 32, 10)
    assert len(notams) == 0


def test_fetchNotamsByAirportCode_no_notams(mock_empty_response: None):
    """Test that fetchNotamsByAirportCode handles the case where API returns no NOTAMs"""
    notam_fetcher = NotamFetcher("CLIENT_ID", "CLIENT_SECRET")
    notams = notam_fetcher.fetch_notams_by_airport_code("LAX")
    assert len(notams) == 0
