#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dweepy
import requests

def main() -> None:
    # the thing name to get dweets from
    # ***CHANGE THIS TO SOMETHING UNIQUE***
    thing_name = "iot-node-0"

    # go into a loop, waiting for dweets
    print()
    print(f"Send a HTTP request to https://dweet.io/dweet/for/{thing_name}?basic=1.23&step=5.67 to see data appearing here")
    while True:
        # Use try except, cos of https://github.com/paddycarey/dweepy/issues/14
        try:
            for dweet in dweepy.listen_for_dweets_from(thing_name):
                print(f"dweet = {dweet}")
        except requests.exceptions.ConnectionError as e:
            print(f"dweet.io closed the connection, reconnecting")

if __name__ == "__main__":
    main()
