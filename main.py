"""Main module."""
from src.data import connection
from src.messaging import gateway,bot



if __name__ == "__main__":
    connection.connect() # connect database
    gateway.main() # start gateway
    bot.polling() # start telebot

