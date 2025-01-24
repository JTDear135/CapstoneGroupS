import pytest
from notam import Notam, NotamKeyword
from datetime import datetime, timezone


def test_notam_init():
    Notam(
        accountability="LAX",
        number="01/177",
        location="LAX",
        keyword=NotamKeyword.TWY,
        issued=datetime(2025, 1, 17, 17, 31),
        effectiveStart=datetime(2025, 1, 24, 8, 30, tzinfo=timezone.utc),
        effectiveEnd=datetime(2025, 1, 24, 14, 30, tzinfo=timezone.utc),
        text="!LAX 01/177 LAX TWY C6 BTN TWY B AND TWY C CLSD 2501240830-2501241430",
        lastUpdated=datetime(2025, 1, 17, 7, 34, tzinfo=timezone.utc),
    )

    Notam(
        accountability="LAX",
        number="04/309",
        location="LAX",
        keyword=NotamKeyword.OBST,
        issued=datetime(2023, 4, 22, 1, 36),
        effectiveStart=datetime(2023, 4, 22, 1, 35, tzinfo=timezone.utc),
        effectiveEnd=datetime(2025, 4, 1, 6, 59, tzinfo=timezone.utc),
        text="!LAX 04/309 LAX OBST SILO (ASN 2023-AWP-696-NRA) 335559N1182236W (1.7NM ESE LAX) 176FT (75FT AGL) LGTD 2304220135-2504010659",
        lastUpdated=datetime(2025, 1, 17, 7, 34, tzinfo=timezone.utc),
    )


def test_notam_init_for_invalid_number():
    with pytest.raises(ValueError, match="Invalid number"):
        notam = Notam(
            accountability="LAX",
            number="01177",
            location="FFFF",
            keyword=NotamKeyword.OBST,
            issued=datetime(2025, 1, 17, 17, 31),
            effectiveStart=datetime(2025, 1, 24, 8, 30, tzinfo=timezone.utc),
            effectiveEnd=datetime(2025, 1, 24, 14, 30, tzinfo=timezone.utc),
        )

def test_notam_init_for_invalid_accountability():
    with pytest.raises(ValueError, match="Invalid accountability"):
        Notam(
            accountability="LZX",
            number="01/177",
            location="LAX",
            keyword=NotamKeyword.OBST,
            issued=datetime(2025, 1, 17, 17, 31),
            effectiveStart=datetime(2025, 1, 24, 8, 30, tzinfo=timezone.utc),
            effectiveEnd=datetime(2025, 1, 24, 14, 30, tzinfo=timezone.utc),
        )

def test_notam_init_for_invalid_location():
    with pytest.raises(ValueError, match="Invalid location"):
        Notam(
            accountability="LAX",
            number="01/177",
            location="LZX",
            keyword=NotamKeyword.OBST,
            issued=datetime(2025, 1, 17, 17, 31),
            effectiveStart=datetime(2025, 1, 24, 8, 30, tzinfo=timezone.utc),
            effectiveEnd=datetime(2025, 1, 24, 14, 30, tzinfo=timezone.utc),
        )