"""mock real-time data and add entries to processed_data table
"""

import time, random
import pandas as pd
from datetime import datetime
import utils
from src.models.processed_data import Processed_data
from src.data import mock_data_historical, session
from config import RAW_DATA_FOLDER_PATH, COMFORT_INDICATORS, CARRIAGE_CAPACITY

# print(session)


def generate_real_time_data():
    passenger_congestion_weekday = pd.read_csv(RAW_DATA_FOLDER_PATH / "passenger_congestion_rate_weekday.csv")
    passenger_congestion_weekend = pd.read_csv(RAW_DATA_FOLDER_PATH / "passenger_congestion_rate_weekend.csv")
    daily_temp_raw = pd.read_csv(RAW_DATA_FOLDER_PATH / "daily_temperature.csv")

    congestion_weekday_seeder = utils.create_seed_data_from_raw_data(passenger_congestion_weekday)
    congestion_weekend_seeder = utils.create_seed_data_from_raw_data(passenger_congestion_weekend)
    daily_temp_seeder  = utils.create_seed_data_from_raw_data(daily_temp_raw) 

    while True:
        indicator = random.choice(COMFORT_INDICATORS)
        current_time = datetime.now()
        curr_time_in_s = utils.convert_hr_min_to_seconds(current_time.hour, current_time.minute)
        if indicator == "crowd":
            if current_time.weekday() in [5, 6]: # weekend
                seed_val = utils.get_seed_value_from_time(congestion_weekend_seeder, curr_time_in_s)
                random_val = mock_data_historical.generate_random_congestion_rate(curr_time_in_s, False, seed_val)
            else: 
                seed_val = utils.get_seed_value_from_time(congestion_weekday_seeder, curr_time_in_s)
                random_val = mock_data_historical.generate_random_congestion_rate(curr_time_in_s, True, seed_val)

            capacity = CARRIAGE_CAPACITY * random.uniform(0.80, 0.95) # if carriage in [1, 4] else CARRIAGE_CAPACITY
            passenger_count = capacity * random_val * 0.01
            new_data = Processed_data(carriage_id=1, comfort_indicator=indicator, value=int(passenger_count), timestamp=utils.convert_epoch_to_datetime(current_time.timestamp()))
            session.add(new_data)
            session.flush()
            session.commit()
        elif indicator == "temperature":
            seed_val = utils.get_seed_value_from_time(daily_temp_seeder, curr_time_in_s)
            random_val = mock_data_historical.generate_random_temp(current_time.timestamp(), seed_val)
            new_data = Processed_data(carriage_id=1, comfort_indicator=indicator, value=int(random_val), timestamp=utils.convert_epoch_to_datetime(current_time.timestamp()))
            session.add(new_data)
            session.flush()
            session.commit()
        elif indicator == "seat":
            last_crowd_data = session.query(Processed_data).filter(Processed_data.comfort_indicator == "crowd").order_by(Processed_data.timestamp.desc()).first()
            random_val = mock_data_historical.calc_seat_availability(last_crowd_data.value)
            new_data = Processed_data(carriage_id=1, comfort_indicator=indicator, value=random_val, timestamp=utils.convert_epoch_to_datetime(current_time.timestamp()))
            session.add(new_data)
            session.flush()
            session.commit()
        else:
            ...


        time.sleep(1)

if __name__ == "__main__":
    ...