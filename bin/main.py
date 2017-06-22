from urllib import quote
from urllib import urlencode

import sqlite3 as sqlite
import yelp
import os
import json
import pprint
import ast
import requests

global conn
global cur
global appPath
global json_contents

appPath = os.getcwd()


class RawDataHandler():
  def __init__(self):
    self.json_contents = yelp.main()
    self.term = self.json_contents["term"]
    self.location = self.json_contents["location"]

  def getRawJSON(self):
    conn = sqlite.connect(appPath + '/data/yelpdb.sqlite')
    cur = conn.cursor()

    cur.execute('''INSERT INTO JSON(SearchJson, ReviewsJson)
    VALUES (?, ?)''', (self.json_contents["searchJson"], self.json_contents["reviewsJson"]))

    conn.commit()

  def writeSearchTable(self):
    conn = sqlite.connect(appPath + '/data/yelpdb.sqlite')
    cur = conn.cursor()

    # convert string on the JSON db to dict with: dictionary = ast.literal_eval(string)
    searchJson = ast.literal_eval(self.json_contents["searchJson"])

    business_count = self.json_contents["total"]

    businessIDs = []
    for i in range(50): #will be range(business_count)
      businessID = searchJson["businesses"][i]["id"]
      cur.execute('''INSERT INTO Search(term, location, business_count, businessID) VALUES (?, ?, ?, ?)''',
      (self.term, self.location, business_count, businessID))
      conn.commit()

      businessIDs.append(businessID)

    return businessIDs

  def writeBusinessTable(self):
    conn = sqlite.connect(appPath + '/data/yelpdb.sqlite')
    cur = conn.cursor()

    # convert string on the JSON db to dict with: dictionary = ast.literal_eval(string)
    searchJson = ast.literal_eval(self.json_contents["searchJson"])

    businessIDs = []
    for i in range(50): #will be range(business_count)
      businessID = searchJson["businesses"][i]["id"]
      name = searchJson["businesses"][i]["name"]
      address = searchJson["businesses"][i]["location"]["address1"]
      city = searchJson["businesses"][i]["location"]["city"]
      country = searchJson["businesses"][i]["location"]["country"]
      zip_code = searchJson["businesses"][i]["location"]["zip_code"]
      url = searchJson["businesses"][i]["url"]
      price = searchJson["businesses"][i]["price"]
      rating = searchJson["businesses"][i]["rating"]
      review_count = searchJson["businesses"][i]["review_count"]
      alias = searchJson["businesses"][i]["categories"][0]["alias"]
      latitude = searchJson["businesses"][i]["coordinates"]["latitude"]
      longitude = searchJson["businesses"][i]["coordinates"]["longitude"]

      cur.execute('''INSERT INTO Business(id, name, address, city, country, zip_code, url, price,
        rating, review_count, alias, latitude, longitude, term, location)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (businessID, name, address, city,
          country, zip_code, url, price, rating, review_count, alias, latitude, longitude,
          self.term, self.location))

      conn.commit()

  def writeReviewsTable(self):
    conn = sqlite.connect(appPath + '/data/yelpdb.sqlite')
    cur = conn.cursor()

    cur.execute("SELECT id FROM Business WHERE term = ? AND location = ?",
      (self.term, self.location))
    IDs = cur.fetchall()

    API_HOST = 'https://api.yelp.com'
    BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
    TOKEN_PATH = '/oauth2/token'

    bearer_token = yelp.obtain_bearer_token(API_HOST, TOKEN_PATH)

    for i in range(len(IDs)):
      business_id = IDs[i][0]
      print "business_id", business_id
      review_path = BUSINESS_PATH + business_id + '/reviews'
      response = yelp.request(API_HOST, review_path, bearer_token)
      reviewsPerBusiness = response["reviews"]
      for review in range(3):
        rating = reviewsPerBusiness[review]["rating"]
        content = reviewsPerBusiness[review]["text"]
        time_created = reviewsPerBusiness[review]["time_created"]
        cur.execute('''INSERT INTO Reviews(business_id, rating, content, time_created, term, location)
        VALUES (?, ?, ?, ?, ?, ?)''', (business_id, rating, content, time_created, self.term, self.location))
        conn.commit()


x = RawDataHandler()
x.getRawJSON()
x.writeSearchTable()
x.writeBusinessTable()
x.writeReviewsTable()
