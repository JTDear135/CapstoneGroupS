import pandas as pd

'''
Flight Code Validator Component

Features:
    - Validates if airport code is valid
    - Validates if airport code is from the United States
    - Validates if airport code is not a part of Alaska or Hawaii
'''

class FlightCodeValidator:
    """
    Validates if airport code is part of United States and not from either Alaska or Hawaii

    Args:
        airport_code (str): Airport Code Accepting Both IATA and ICAO Format

    Returns:
        True: Valid United States Airport
        False: Airport Outside of United States, From Alaska, From Hawaii, Or Does Not Exist.
    """
    def is_valid(airport_code: str):
        columns = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone", "DST", "Tz Database Timezone", "Type", "Source"]
        df = pd. read_csv("airports.dat", header=None)
        if airport_code in df[4].values:
            airport_details = df.loc[df[4] == airport_code]
            # Checks from United States
            if "United States" in airport_details[3].values:
                # Checks from Hawaii
                if "Pacific/Honolulu" in airport_details[11].values:
                    return False
                # Checks from Alaska
                elif "America/Anchorage" in airport_details[11].values:
                    return False
                else:
                    return True
            # Not from United States
            else:
                    return False
        elif airport_code in df[5].values:
            airport_details = df.loc[df[5] == airport_code]
            # Checks from United States
            if "United States" in airport_details[3].values:
                print("I Am From The United States")
                if "Pacific/Honolulu" in airport_details[11].values:
                    # Checks from Hawaii
                    return False
                elif "America/Anchorage" in airport_details[11].values:
                    # Checks from Alaska
                    return False
                else:
                    return True
            # Not from United States
            else:
                return False
        # Airport does not exist
        else:
            return False