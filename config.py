import datetime
import os
from pathlib import Path


ROOT_DIR = Path(os.path.realpath(os.path.join(os.path.dirname(__file__))))
RAW_DATA_FOLDER_PATH = ROOT_DIR / "data" / "raw"
INTERM_DATA_FOLDER_PATH = ROOT_DIR / "data" / "intermediate"


# general
COMFORT_INDICATORS = [None, "seat", "crowd", "temperature"]
INTERVAL_MINUTES = 3
SECONDS_BIN = [sec for sec in range(0, 24*60*60, INTERVAL_MINUTES*60)]
CLOSING_TIME = 0.25 * 60 * 60
OPENING_TIME = 5.5 * 60 * 60
START_DATE = int(datetime.datetime(2021, 10, 1).timestamp())
today = datetime.datetime.today()
END_DATE = int(datetime.datetime(today.year, today.month, today.day).timestamp())
CARRIAGE_CAPACITY = 40
CARRIAGE_IDS = [i+1 for i in range(4)]


# Crowdedness
WD_NON_PEAK_VARIATION = 0.15
WD_PEAK_VARIATION = 0.05
WE_NON_PEAK_VARIATION = 0.25
WE_PEAK_VARIATION = 0.1
# peak period weekdays: 7am - 930am, 530-830pm
WD_PEAK_1_START = 7 * 60 * 60
WD_PEAK_1_END = 9.5 * 60 * 60 
WD_PEAK_2_START = 17.5 * 60 * 60
WD_PEAK_2_END = 20.5 * 60 * 60
# peak period weekend: 8am - 930am, 630-830pm
WE_PEAK_1_START = 8 * 60 * 60
WE_PEAK_1_END = 9.5 * 60 * 60
WE_PEAK_2_START = 18.5 * 60 * 60 
WE_PEAK_2_END = 20.5 * 60 * 60



# temperature
HOT_MONTHS = [1,2,3,7,8]
COLD_MONTHS = [11,12]
COLDEST_TEMP = 23
HOTTEST_TEMP = 30
TEMP_VARIATION = 0.10


# seat availability
SEATS_PER_CARRIAGE = 20
