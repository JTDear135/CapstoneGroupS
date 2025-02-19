'''
This Script Calls the Airport db, and creates a holistic Airport List in the form of a CSV
'''

import pandas as pd

url = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat"

columns = [ "Airport ID", "Name", "City", "Country", "IATA", "ICAO","Latitude", "Longitude", "Altitude", "Timezone", "DST","Tz database timezone", "Type", "Source"]

# Read the dataset with proper quoting and separator handling
df = pd.read_csv(
    url,
    names=columns,
    header=None,
    keep_default_na=False,
    on_bad_lines="skip", # skips the badly formatted ones, so essentially this is not the best implementation
    quoting=3,
    low_memory=False
)

# Convert numeric columns properly while keeping others as strings
df["Airport ID"] = pd.to_numeric(df["Airport ID"], errors='coerce')
df["Latitude"] = pd.to_numeric(df["Latitude"], errors='coerce')
df["Longitude"] = pd.to_numeric(df["Longitude"], errors='coerce')
df["Altitude"] = pd.to_numeric(df["Altitude"], errors='coerce')

# Strip extra spaces and remove quotes
df[df.select_dtypes(include=['object']).columns] = df.select_dtypes(include=['object']).apply(
    lambda x: x.str.strip().str.replace('"', '', regex=False)
)

# Print the actual shape to verify the number of rows
print(f"Total rows: {df.shape[0]}")

# Save to CSV
csv_filename = "airports_data.csv"
df.to_csv(csv_filename, index=False)

print(f"CSV file saved as {csv_filename}")
