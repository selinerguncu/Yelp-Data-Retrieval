from urllib import quote
from urllib import urlencode
from rawDataHandler import RawDataHandler
from geopy import Point
from geopy.distance import distance, VincentyDistance

import sqlite3 as sqlite
import yelpQuery
import os
import json
import pprint
import time
import sys
import ast
import requests
import areaCoordinates

global conn
global cur
# global appPath
global json_contents

# appPath = os.getcwd()

coordinates = areaCoordinates.area

categories = ["restaurants", "bars", "nightlife", "coffee", "beautysvc", "food", "giftshops"]
# categories = ["restaurants", "bars", "nightlife", "coffee", "beautysvc", "food"]
prices = ["1", "2", "3", "4"]
# categories = ["restaurants"]
# prices = ["1"]

# LATT_INCREMENT = 0.005
# LONG_INCREMENT = 0.005

#mainland coordinates:
LATT_WEST = 44.81314
LATT_EAST = 25.11735
LATT_NORTH = 49.2666656
LATT_SOUTH = 48.16590

LONG_WEST = -66.96276
LONG_EAST = -81.08813
LONG_NORTH = -95.0499998
LONG_SOUTH = -124.73246

def checkIfValidCoordinate(latOrLong, coordinate):
  isValid = False
  for coordinateSet in coordinates:
    if latOrLong == 'lat':
      if coordinateSet["lat"][0] > coordinate > coordinateSet["lat"][1]:
        isValid = True
        break
    else:
      if coordinateSet["lng"][1] > coordinate > coordinateSet["lng"][0]:
        isValid = True
        break

  return isValid


#Bay area coordinates:
BORDERS = {
  'NW': (37.95077976072001, -122.74698257446289),
  'NE': (38.04601261075696, -122.07544326782227),
  'SE': (37.16149648300589, -121.47668838500977),
  'SW': (37.0421100532159, -122.42425918579102)
}

input_values = {}

i = 0
j = 0
for price in prices:
  input_values["price"] = price

  for category in categories:
    input_values["category"] = category

    latitude = BORDERS["NW"][0]

    while BORDERS["NW"][0] >= latitude >= BORDERS["SW"][0]:
      longitude = BORDERS["NW"][1]
      latValid = checkIfValidCoordinate('lat', latitude)

      newPoint = VincentyDistance(kilometers=0.353).destination(Point(latitude, longitude), 180)

      if latValid:
        input_values["latitude"] = latitude
        latitude = newPoint.latitude
      else:
        latitude = newPoint.latitude
        continue


      while BORDERS["NE"][1] >= longitude >= BORDERS["NW"][1]:
        j += 1
        longValid = checkIfValidCoordinate('lng', longitude)
        newPoint = VincentyDistance(kilometers=0.353).destination(Point(latitude, longitude), 90)
        if longValid:
          input_values["longitude"] = longitude
          longitude = newPoint.longitude
          i = i + 1
          if 23000 < i < 28000:
            time.sleep(0.1)
            print i
            area = RawDataHandler(input_values)
            area.getRawJSON()
            area.writeSearchTable()
            area.writeBusinessTable()
            area.writeReviewsTable()
          elif i >= 28000:
            print '---'
            print i
            sys.exit()
        else:
          longitude = newPoint.longitude
          continue

