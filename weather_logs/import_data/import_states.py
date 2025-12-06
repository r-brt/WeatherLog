import pandas as pd
from weather_logs.models import State

def run():
    # Read CSV file into a DataFrame
    csv_file_path = 'weather_logs/import_data/States.csv'
    df = pd.read_csv(csv_file_path)

    # Iterate through the DataFrame and create model instances
    for index, row in df.iterrows():
        # Create the State instance
        state = State(
            name=row['NAME'],
            abbreviation=row['ABBREVIATION'],
        )
        state.save()

    print("State CSV data has been loaded into the Django database.")
