import pandas as pd
import random, datetime, io, os
from src.models.processed_data import Processed_data
import utils
from config import RAW_DATA_FOLDER_PATH, INTERM_DATA_FOLDER_PATH, WD_PEAK_1_START, WD_PEAK_1_END, WD_PEAK_2_START, WD_PEAK_2_END, WD_PEAK_VARIATION, WD_NON_PEAK_VARIATION, WE_PEAK_1_START, WE_PEAK_1_END, WE_PEAK_2_START, WE_PEAK_2_END, WE_PEAK_VARIATION, WE_NON_PEAK_VARIATION, START_DATE, END_DATE, CARRIAGE_IDS, CARRIAGE_CAPACITY, HOT_MONTHS, COLD_MONTHS, TEMP_VARIATION, HOTTEST_TEMP, COLDEST_TEMP, SEATS_PER_CARRIAGE
from src.data import engine, session



def generate_random_congestion_rate(time_in_day_s: int, is_weekday: bool, seed_value: float):
    if is_weekday:
        if WD_PEAK_1_START <= time_in_day_s <= WD_PEAK_1_END or WD_PEAK_2_START <= time_in_day_s <= WD_PEAK_2_END:
            upper_bound = seed_value * (1 + WD_PEAK_VARIATION)
            lower_bound = seed_value * (1 - WD_PEAK_VARIATION)
        else:
            upper_bound = seed_value * (1 + WD_NON_PEAK_VARIATION)
            lower_bound = seed_value * (1 - WD_NON_PEAK_VARIATION)
    else:
        if WE_PEAK_1_START <= time_in_day_s <= WE_PEAK_1_END or WE_PEAK_2_START <= time_in_day_s <= WE_PEAK_2_END:
            upper_bound = seed_value * (1 + WE_PEAK_VARIATION)
            lower_bound = seed_value * (1 - WE_PEAK_VARIATION)
        else:
            upper_bound = seed_value * (1 + WE_NON_PEAK_VARIATION)
            lower_bound = seed_value * (1 - WE_NON_PEAK_VARIATION)

    if upper_bound > 100: upper_bound = 100
    if lower_bound > 100: lower_bound = 100
    if upper_bound < 0: upper_bound = 0
    if lower_bound < 0: lower_bound = 0

    return random.uniform(lower_bound, upper_bound)



def generate_random_values_daily(seed_df, times_in_s, is_weekday):
    random_vals = []
    for time_in_s in times_in_s:
        seed_val = utils.get_seed_value_from_time(seed_df, time_in_s)
        random_val = generate_random_congestion_rate(time_in_s, is_weekday, seed_val)
        random_vals.append(random_val)
    return random_vals



def generate_historical_congestion_data(weekday_data_seeder, weekend_data_seeder, carriage_id):
    full_df = pd.DataFrame()

    for day in range(START_DATE, END_DATE, 86400):
        random_times = utils.generate_random_times_in_day()
        is_weekday = datetime.datetime.fromtimestamp(day).weekday() in [i for i in range(5)]
        if is_weekday:
            random_vals = generate_random_values_daily(weekday_data_seeder, random_times, is_weekday)
        else:
            random_vals = generate_random_values_daily(weekend_data_seeder, random_times, is_weekday)
            
        daily_congestion_df = pd.DataFrame({"time": random_times, "value": random_vals})
        daily_congestion_df.time = daily_congestion_df.time + day
        full_df = pd.concat([full_df, daily_congestion_df], axis=0)
    full_df["carriage_id"] = carriage_id
    return full_df



def generate_historical_congestion_data_all_carriages(congestion_weekday_seeder, congestion_weekend_seeder):
    all_carriages = pd.DataFrame()
    for carriage in CARRIAGE_IDS:
        carriage_df = generate_historical_congestion_data(congestion_weekday_seeder, congestion_weekend_seeder, carriage)
        
        capacity = CARRIAGE_CAPACITY * random.uniform(0.80, 0.95) if carriage in [1, 4] else CARRIAGE_CAPACITY
        carriage_df["value"] = capacity * carriage_df["value"] * 0.01
        all_carriages = pd.concat([all_carriages, carriage_df])

    all_carriages["value"] = all_carriages["value"].astype(int)

    # all_carriages.time = all_carriages.time.apply(convert_epoch_to_datetime)
    all_carriages["comfort_indicator"] = "crowd"
    all_carriages.rename(columns={"time": "timestamp"}, inplace=True)
    return all_carriages







def generate_random_temp(epoch_day: int, seed_value: float):

    if datetime.datetime.fromtimestamp(epoch_day).month in HOT_MONTHS:
        upper_bound = seed_value * (1 + TEMP_VARIATION)
        lower_bound = seed_value
    elif datetime.datetime.fromtimestamp(epoch_day).month in COLD_MONTHS:
        upper_bound = seed_value 
        lower_bound = seed_value * (1 - TEMP_VARIATION)
    else:
        upper_bound = seed_value * (1 + 0.5 * TEMP_VARIATION)
        lower_bound = seed_value * (1 - 0.5 * TEMP_VARIATION)

    if upper_bound > HOTTEST_TEMP: upper_bound = HOTTEST_TEMP
    if lower_bound > HOTTEST_TEMP: lower_bound = HOTTEST_TEMP
    if upper_bound < COLDEST_TEMP: upper_bound = COLDEST_TEMP
    if lower_bound < COLDEST_TEMP: lower_bound = COLDEST_TEMP

    return random.uniform(lower_bound, upper_bound)



def generate_random_temp_values_daily(seed_df, times_in_s, epoch_day: int):
    random_vals = []
    for time_in_s in times_in_s:
        seed_val = utils.get_seed_value_from_time(seed_df, time_in_s)
        random_val = generate_random_temp(epoch_day, seed_val)
        random_vals.append(random_val)
    return random_vals


def generate_historical_temp_data(temp_data_seeder, carriage_id):
    full_df = pd.DataFrame()

    for day in range(START_DATE, END_DATE, 86400):
        random_times = utils.generate_random_times_in_day()
        random_vals = generate_random_temp_values_daily(temp_data_seeder, random_times, day)
            

        daily_temp_df = pd.DataFrame({"time": random_times, "value": random_vals})
        daily_temp_df.time = daily_temp_df.time + day
        full_df = pd.concat([full_df, daily_temp_df], axis=0)
    full_df["carriage_id"] = carriage_id
    return full_df

def generate_historical_temp_all_carriages(daily_temp_seeder):
    all_carriages = pd.DataFrame()
    for carriage in CARRIAGE_IDS:
        carriage_df = generate_historical_temp_data(daily_temp_seeder, carriage)
        
        carriage_df["value"] = carriage_df["value"] * random.uniform(0.95, 1.0) if carriage in [1, 4] else carriage_df["value"]
        all_carriages = pd.concat([all_carriages, carriage_df])

    all_carriages["value"] = all_carriages["value"].astype(float)

    # all_carriages.time = all_carriages.time.apply(convert_epoch_to_datetime)
    all_carriages["comfort_indicator"] = "temperature"
    all_carriages.rename(columns={"time": "timestamp"}, inplace=True)
    return all_carriages







def calc_seat_availability(passenger_count):
    if 0 < passenger_count <= SEATS_PER_CARRIAGE:
        lower_bound = SEATS_PER_CARRIAGE - passenger_count
        upper_bound = SEATS_PER_CARRIAGE
    else:
        lower_bound = 0
        upper_bound = 0

    return random.randint(lower_bound, upper_bound)



def generate_and_combine_historical_data():
    print("Generating historical data...")
    if os.path.exists(INTERM_DATA_FOLDER_PATH / "historical_combined.csv"):
        print(f"Historical data already exists at {INTERM_DATA_FOLDER_PATH}, will not regenerate.")
        return pd.read_csv(INTERM_DATA_FOLDER_PATH / "historical_combined.csv")

    passenger_congestion_weekday = pd.read_csv(RAW_DATA_FOLDER_PATH / "passenger_congestion_rate_weekday.csv")
    passenger_congestion_weekend = pd.read_csv(RAW_DATA_FOLDER_PATH / "passenger_congestion_rate_weekend.csv")
    daily_temp_raw = pd.read_csv(RAW_DATA_FOLDER_PATH / "daily_temperature.csv")

    congestion_weekday_seeder = utils.create_seed_data_from_raw_data(passenger_congestion_weekday)
    congestion_weekend_seeder = utils.create_seed_data_from_raw_data(passenger_congestion_weekend)
    daily_temp_seeder  = utils.create_seed_data_from_raw_data(daily_temp_raw) 

    crowd_historical_df = generate_historical_congestion_data_all_carriages(congestion_weekday_seeder, congestion_weekend_seeder)
    temp_historical_df = generate_historical_temp_all_carriages(daily_temp_seeder)

    seat_availability_df = crowd_historical_df.copy(deep=True)
    seat_availability_df.timestamp = seat_availability_df.timestamp + 1
    seat_availability_df["value"] = seat_availability_df.value.apply(calc_seat_availability)
    seat_availability_df["comfort_indicator"] = "seat"

    historical_combined = pd.DataFrame()
    historical_combined = pd.concat([historical_combined, crowd_historical_df, temp_historical_df, seat_availability_df])
    historical_combined.timestamp = historical_combined.timestamp.apply(utils.convert_epoch_to_datetime)
    # historical_combined["id"] = range(1, len(historical_combined)+1)
    historical_combined = historical_combined[['carriage_id', 'comfort_indicator', 'value', 'timestamp']]
    # historical_combined = historical_combined[['id', 'carriage_id', 'comfort_indicator', 'value', 'timestamp']]
    # historical_combined.set_index("id", inplace=True)
    print(f"TEST {historical_combined.columns}")
    historical_combined.to_csv(INTERM_DATA_FOLDER_PATH / "historical_combined.csv", encoding="utf_8_sig", index=False)

    with session as sesh:
        sesh.bulk_insert_mappings(Processed_data, historical_combined.to_dict('records'))
        sesh.commit()
    sesh.close()

    print("Inserted historical data to processed_data table")
    return historical_combined