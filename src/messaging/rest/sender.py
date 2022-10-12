#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dweepy
import pprint

def main() -> None:
    # the thing name to send dweets to
    # ***CHANGE THIS TO SOMETHING UNIQUE***
    thing_name = "iot-node-0" 

    # send dweet, get response
    # response tells you whether the dweet was successful or not
    response = dweepy.dweet_for(thing_name, {'light': '5.67', 'status' : 'bright'})

    print(f"dweet's response:")
    pprint.pprint(response)

    print(f"Send a HTTP request to https://dweet.io/get/latest/dweet/for/{thing_name} to see the dweet")
    print()


if __name__ == "__main__":
    main()
