#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nis import match
import requests
import serial
import csv
import os
import subprocess
import json
import re
import paho.mqtt.client as mqtt
import sys
import logging
import argparse
import getpass
import random
import urllib
import pprint
import sched
import time
import datetime
import threading
#from src.models.light import Light
import src.models as model
from src.data import session
from src.data import connection
from src.data import data_operator

# Configure logging
logging.basicConfig(format="%(asctime)s %(levelname)s %(filename)s:%(funcName)s():%(lineno)i: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)
logger = logging.getLogger(__name__)

mqttc = None

GATEWAY = {
    "name": "iot-hexagon",
}

# ====================================================
# MQTT Settings
MQTT_Broker = "iot.eclipse.org"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic_Humidity = "Home/BedRoom/DHT22/Humidity"
MQTT_Topic_Temperature = "Home/BedRoom/DHT22/Temperature"


# ====================================================


# Handles the case when the serial port can't be found
def handle_missing_serial_port() -> None:
    print("Couldn't connect to the micro:bit. Try these steps:")
    print("1. Unplug your micro:bit")
    print("2. Close Tera Term, PuTTY, and all other apps using the micro:bit")
    print("3. Close all MakeCode browser tabs using the micro:bit")
    print("4. Run this app again")
    exit()


# Initializes the serial device. Tries to get the serial port that the micro:bit is connected to
def get_serial_dev_name() -> str:
    logger.info(f"sys.platform: {sys.platform}")
    logger.info(f"os.uname().release: {os.uname().release}")
    logger.info("")

    serial_dev_name = None
    if "microsoft" in os.uname().release.lower():  # Windows Subsystem for Linux

        # List the serial devices available
        try:
            stdout = subprocess.check_output(
                "pwsh.exe -Command '[System.IO.Ports.SerialPort]::getportnames()'", shell=True).decode("utf-8").strip()
            if not stdout:
                handle_missing_serial_port()
        except subprocess.CalledProcessError:
            logger.error(
                f"Couldn't list serial ports: {e.output.decode('utf8').strip()}")
            handle_missing_serial_port()

        # Guess the serial device
        stdout = stdout.splitlines()[-1]
        serial_dev_name = re.search("COM([0-9]*)", stdout)
        if serial_dev_name:
            serial_dev_name = f"/dev/ttyS{serial_dev_name.group(1)}"

    elif "linux" in sys.platform.lower():  # Linux

        # List the serial devices available
        try:
            stdout = subprocess.check_output(
                "ls /dev/ttyACM*", stderr=subprocess.STDOUT, shell=True).decode("utf-8").strip()
            if not stdout:
                handle_missing_serial_port()
        except subprocess.CalledProcessError as e:
            logger.error(
                f"Couldn't list serial ports: {e.output.decode('utf8').strip()}")
            handle_missing_serial_port()

        # Guess the serial device
        serial_dev_name = re.search("(/dev/ttyACM[0-9]*)", stdout)
        if serial_dev_name:
            serial_dev_name = serial_dev_name.group(1)

    elif sys.platform == "darwin":  # macOS

        # List the serial devices available
        try:
            stdout = subprocess.check_output(
                "ls /dev/cu.usbmodem*", stderr=subprocess.STDOUT, shell=True).decode("utf-8").strip()
            if not stdout:
                handle_missing_serial_port()
        except subprocess.CalledProcessError:
            logger.error(
                f"Error listing serial ports: {e.output.decode('utf8').strip()}")
            handle_missing_serial_port()

        # Guess the serial device
        serial_dev_name = re.search("(/dev/cu.usbmodem[0-9]*)", stdout)
        if serial_dev_name:
            serial_dev_name = serial_dev_name.group(1)

    else:
        logger.error(f"Unknown sys.platform: {sys.platform}")
        exit()

    logger.info(f"serial_dev_name: {serial_dev_name}")
    logger.info("Serial ports available:")
    logger.info("")
    logger.info(stdout)

    if not serial_dev_name:
        handle_missing_serial_port()

    return serial_dev_name


# Handles an MQTT client connect event
# This function is called once just after the mqtt client is connected to the server.
def handle_mqtt_connack(client, userdata, flags, rc) -> None:
    logger.debug(f"MQTT broker said: {mqtt.connack_string(rc)}")
    if rc == 0:
        client.is_connected = True

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(f"{GATEWAY['name']}/control")
    logger.info(f"Subscribed to: {GATEWAY['name']}/control")
    logger.info(
        f"Publish something to {GATEWAY['name']}/control and the messages will appear here.")


# Handles an incoming message from the MQTT broker.
def handle_mqtt_message(client, userdata, msg) -> None:
    logger.info(
        f"received msg | topic: {msg.topic} | payload: {msg.payload.decode('utf8')}")


# Handles incoming serial data
def handle_serial_data(s: serial.Serial) -> None:
    print(s)
    payload = s.readline().decode("utf-8").strip()
    # Publish data to MQTT broker
    logger.info(
        f"Publish | topic: {GATEWAY['name']}/sensors | payload: {payload}")
    #    mqttc.publish(topic=f"{GATEWAY['name']}/sensors", payload=payload, qos=0)
    vals = payload.split("|")
    # update sensor reading data
    if vals[0] != 'CDr':
        data_operator.add_record(vals,session)

    if vals[0] == 'CD':
        print(vals)
        data_operator.count_crowd(vals,connection,session)

    if vals[0] == 'SA':
        data_operator.count_seat(vals,connection,session)

    if vals[0] == 'TP':
        data_operator.update_temp(vals,session)

    print(payload)



def main() -> None:
    global mqttc

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--device", type=str,
                        help="serial device to use, e.g. /dev/ttyS5")

    args = parser.parse_args()
    args_device = args.device

    # Create mqtt client
    mqttc = mqtt.Client()

    # Register callbacks
    mqttc.on_connect = handle_mqtt_connack
    mqttc.on_message = handle_mqtt_message

    # Connect to broker
    # mqttc.is_connected = False
    # mqttc.connect("broker.mqttdashboard.com")
    # mqttc.loop_start()
    # time_to_wait_secs = 1
    # while not mqttc.is_connected and time_to_wait_secs > 0:
    #     time.sleep(0.1)
    #     time_to_wait_secs -= 0.1

    # if time_to_wait_secs <= 0:
    #     logger.error(f"Can't connect to broker.mqttdashboard.com")
    #     return

    # Try to get the serial device name
    if args.device:
        serial_dev_name = args.device
    else:
        serial_dev_name = get_serial_dev_name()

    with serial.Serial(port=serial_dev_name, baudrate=115200, timeout=10) as s:
        # Sleep to make sure serial port has been opened before doing anything else
        time.sleep(1)

        # Reset the input and output buffers in case there is leftover data
        s.reset_input_buffer()
        s.reset_output_buffer()

        # Loopy loop
        while True:

            # Read from the serial port
            if s.in_waiting > 0:
                handle_serial_data(s)

    mqttc.loop_stop()


if __name__ == "__main__":
    main()

# 1/1/1/
# train_id/carriage_id/door_id/temperature/sensor_id
# train_id/carriage_id/door_id/sound/sensor_id
# train_id/carriage_id/door_id/light/sensor_id
# train_id/carriage_id/door_id/pir/sensor_id/in (or out)
# train_id/carriage_id/seat_id
