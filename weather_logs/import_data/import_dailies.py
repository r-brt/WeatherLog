import pandas as pd
import glob
import numpy as np
from weather_logs.models import Station, DailyTemp

def run():
    # Read CSV file into a DataFrame
    # Get CSV files list from a folder
    path = 'weather_logs/import_data'
    csv_files = glob.glob(path + "/*DC_Dailies.csv")
    # csv_file_path = 'weather_logs/import_data/2023_Virginia_Dailies_2.csv'

    df_list = (pd.read_csv(file) for file in csv_files)

    for file in csv_files:

        df = pd.read_csv(file)

        df.replace(np.nan, None, inplace=True)

        # Iterate through the DataFrame and create model instances
        for index, row in df.iterrows():
            # Check if this date already exists for this station before creating
            station = Station.objects.get(station_id=row['STATION'])
            new_date = pd.to_datetime(row['DATE'], format='%m/%d/%Y')
            if len(DailyTemp.objects.filter(station_id=station, date=new_date)) == 0:
                daily = DailyTemp(
                    station_id=station,
                    date=new_date,
                    temp_avg=row['TAVG'],
                    temp_max=row['TMAX'],
                    temp_min=row['TMIN'],
                )
                daily.save()
            else:
                print("Skipped Station: "+row['STATION'])

        print("Dailies CSV data has been loaded into the Django database: "+file)
