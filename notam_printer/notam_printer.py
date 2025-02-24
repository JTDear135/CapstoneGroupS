from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, alias_generators
from rich.console import Console

# NotAM class copied from notam_fetcher/api_schema.py
class Notam(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel
    )
    
    id: str
    number: str
    type: str
    issued: datetime
    selection_code: Optional[str]
    location: str
    effective_start: datetime
    effective_end: datetime | str
    text: str
    classification: str
    account_id: str
    last_updated: datetime
    icao_location: str

def formatNotam(notam: Notam):
    """
    Formats a NotAM object into a legible string representation.

    Args:
        notam (Notam): The Notam object to format
    
    Returns:
        str: A formatted string representation of the Notam object
    """

    # Handling effective_end since it can be a string as well as a datetime object
    effective_end = (
        notam.effective_end.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(notam.effective_end, datetime)
        else notam.effective_end
    )

    return (
        f"ID: {notam.id}\n"
        f"Number: {notam.number}\n"
        f"Type: {notam.type}\n"
        f"Issued: {notam.issued.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Selection Code: {notam.selection_code}\n"
        f"Location: {notam.location}\n"
        f"Effective Start: {notam.effective_start.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Effective End: {effective_end}\n"
        f"Classification: {notam.classification}\n"
        f"Account ID: {notam.account_id}\n"
        f"Last Updated: {notam.last_updated.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"ICAO Location: {notam.icao_location}\n"
        f"Text: {notam.text}\n"
        f"{'-' * 40}"
    )

def print_notams(notams: List[Notam]):

    """
    Takes a list of Notams and prints them in a legible format

    Args:
        notams (List[Notam]): A list of NOTAMs to be printed
    """

    console = Console()
    for notam in notams:
        console.print(formatNotam(notam))
        console.print()
        console.print("-" * 80)
        console.print()

notams = [
    Notam(
    id="2",
    number="B5678",
    type="Restriction",
    issued=datetime(2025, 3, 1, 15, 30, 0),
    selection_code="X123",
    location="LAX",
    effective_start=datetime(2025, 3, 2, 6, 0, 0),
    effective_end=datetime(2025, 3, 5, 20, 0, 0),
    text="Airspace restriction in effect due to military exercise.",
    classification="Airspace",
    account_id="ABC456",
    last_updated=datetime(2025, 3, 1, 16, 0, 0),
    icao_location="KLAX"
)
]

print_notams(notams)