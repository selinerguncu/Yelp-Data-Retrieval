from urllib import quote
from urllib import urlencode
from rawDataHandler import RawDataHandler

import sqlite3 as sqlite
import yelpQuery
import os
import json
import pprint
import ast
import requests

global conn
global cur
# global appPath
global json_contents

# appPath = os.getcwd()

# categories = ["restaurants", "bars", "nightlife", "coffee", "beautysvc", "food", "giftshops"]
categories = ["restaurants", "bars", "nightlife", "coffee"]
prices = ["1", "2", "3", "4"]

LATT_INCREMENT = 0.015
LONG_INCREMENT = 0.015

#mainland coordinates:
LATT_WEST = 44.81314
LATT_EAST = 25.11735
LATT_NORTH = 49.2666656
LATT_SOUTH = 48.16590

LONG_WEST = -66.96276
LONG_EAST = -81.08813
LONG_NORTH = -95.0499998
LONG_SOUTH = -124.73246

#sample area in SF coordinates:
# LATT_WEST = 37.7807
# LATT_EAST = 37.75499
# LATT_NORTH = 37.78835
# LATT_SOUTH = 37.74413

# LONG_WEST = -122.5087
# LONG_EAST = -122.3937
# LONG_NORTH = -122.40760
# LONG_SOUTH = -122.501549

input_values = {}


i = 0
for price in prices:
  input_values["price"] = price
  # print "-----------------", price
  for category in categories:
    west = LATT_WEST
    input_values["category"] = category
    # print "++++++++++++++++++++", category

    while west > LATT_EAST:
      north = LONG_NORTH
      latitude = west
      input_values["latitude"] = latitude
      west = west - LATT_INCREMENT
      while north > LONG_SOUTH:
        longitude = north
        input_values["longitude"] = longitude

        i = i + 1
        # print i
        # print north, west
        area = RawDataHandler(input_values)
        area.getRawJSON()
        area.writeSearchTable()
        area.writeBusinessTable()
        area.writeReviewsTable()

        north = north - LONG_INCREMENT
