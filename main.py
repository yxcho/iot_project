"""Main module."""
from src.data import connection, mock_data_rt, mock_data_historical
from src.messaging import gateway


if __name__ == "__main__":
    connection.connect() # connect database
    mock_data_historical.generate_and_combine_historical_data()
    gateway.main() # start gateway
    mock_data_rt.generate_real_time_data()
    # bot.polling() # start telebot

