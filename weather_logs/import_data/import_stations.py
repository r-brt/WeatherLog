import pandas as pd
import numpy as np
from weather_logs.models import Station, State

def run():
    # Read CSV file into a DataFrame
    csv_file_path = 'weather_logs/import_data/2024_DC_Stations.csv'
    df = pd.read_csv(csv_file_path)

    df.replace(np.nan, None, inplace=True)

    # Iterate through the DataFrame and create model instances
    for index, row in df.iterrows():
        # Check if station is in Table before creating
        if len(Station.objects.filter(station_id=row['STATION'])) == 0:
            station = Station(
                station_id=row['STATION'],
                name=row['NAME'],
                latitude=row['LATITUDE'],
                longitude=row['LONGITUDE'],
                elevation = row['ELEVATION'],
                state = State.objects.get(name__iexact=(row['STATE'])),
            )
            station.save()
        else:
            print("Skipped Station: "+row['STATION'])

    print("Station CSV data has been loaded into the Django database.")
