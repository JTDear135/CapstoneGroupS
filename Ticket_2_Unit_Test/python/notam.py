from datetime import datetime
from enum import Enum
from typing import Optional


class NotamKeyword(Enum):
    RWY="RWY" # Runway
    IAP="IAP" # Instrument Approach Procedure
    VFP="VFP" # Visual Flight Procedure
    DVA="DVA" # Diverse Vector Area
    TWY="TWY" # Taxiway
    AD="AD" # Aerodrome
    OBST="OBST" # Obstruction
    NAV="NAV" # Navigation
    COM="COM" # Communication
    SVC="SVC" # Services
    ODP="ODP" # Obstacle Departure Procedure
    SID="SID" # Standard Instrument Departure
    STAR="STAR" # Standard Terminal Arrival
    CHART="CHART"
    DATA="DATA"
    AIRSPACE="AIRSPACE"
    SPECIAL="SPECIAL"
    SECURITY="SECURITY"
    ROUTE="ROUTE"
    APRON="APRON" 

class Notam:
    """Represents a Notice to Air Missions (NOTAM)."""
    def __init__(
        self,
        accountability: str,
        number: str,
        location: str,
        keyword: NotamKeyword,
        issued: datetime,
        effectiveStart: datetime,
        effectiveEnd: datetime,
        text: Optional[str] = None,
        lastUpdated: Optional[datetime] = None,
    ):
        self.accountability = accountability
        self.number = number
        self.location = location
        self.keyword = keyword 
        self.issued = issued
        self.effectiveStart = effectiveStart
        self.effectiveEnd = effectiveEnd
        self.text = text
        self.lastUpdated = lastUpdated
        