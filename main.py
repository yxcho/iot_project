"""Main module."""
from src.data import connection
from src.messaging import gateway



if __name__ == "__main__":
    connection.connect() # connect database
    gateway.main() # start gateway

