import math, random, datetime
import numpy as np
from config import CLOSING_TIME, OPENING_TIME, SECONDS_BIN, INTERVAL_MINUTES


def convert_hr_min_to_seconds(hr, min):
    return hr * 60 * 60 + min * 60

def convert_float_to_seconds(time_float):
    hour = math.floor(time_float)
    minute = 60 * (time_float - hour)
    return hour * 60 * 60 + minute * 60


def generate_random_times_in_day():
    START = 0
    END = 1 * 60 * 60 * 24
    K = int(86400 / 300)
    time_in_s = random.sample(range(START, END), K)
    return sorted(set(time_in_s))


def convert_epoch_to_datetime(epoch_time: int):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M:%S')



def get_seed_value_from_time(seed_value_df, time_in_day_s):
    if 0 <= time_in_day_s <= CLOSING_TIME or OPENING_TIME <= time_in_day_s <= 23.999 * 60 * 60:
        result_index = seed_value_df['time_bin_s'].sub(time_in_day_s).abs().idxmin()
        return seed_value_df.rate[result_index]
    else: return 0

def create_seed_data_from_raw_data(raw_data_df):
    raw_data_df["time"] = raw_data_df["time"].apply(convert_float_to_seconds)
    raw_data_df["time_bin"] = np.digitize(raw_data_df["time"], SECONDS_BIN)
    raw_data_seeder = raw_data_df.groupby("time_bin").mean().reset_index()
    raw_data_seeder["time_bin_s"] = raw_data_seeder["time_bin"] * INTERVAL_MINUTES * 60
    raw_data_seeder.drop(columns=["time", "time_bin"], inplace=True)
    raw_data_seeder.rename(columns={"value":"rate"}, inplace=True)
    raw_data_seeder = raw_data_seeder[["time_bin_s", "rate"]]
    return raw_data_seeder