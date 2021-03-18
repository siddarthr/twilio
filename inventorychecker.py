import requests
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
import json 
import time
from twilio.rest import Client

account_sid  = "XYZ"
auth_token  = "ABC"
client = Client(account_sid, auth_token)
lastcheck= "unavailable"
while(True):
    try:
        r = requests.get('https://api.target.com/fulfillment_aggregator/v1/fiats/81114595?key=ff457966e64d5e877fdbad070f276d18ecec4a01&nearby=98052&limit=20&requested_quantity=1&radius=50&fulfillment_test_mode=grocery_opu_team_member_test')
        #r = requests.get('https://api.target.com/fulfillment_aggregator/v1/fiats/81114477?key=ff457966e64d5e877fdbad070f276d18ecec4a01&nearby=98105&limit=20&requested_quantity=1&radius=50&fulfillment_test_mode=grocery_opu_team_member_test')
        fullresponse = r.json()
        str = json.dumps(fullresponse)
        ## if in stock
        if str.find("IN_STOCK") != -1:
            #print("in stock")
            ## send sms only when different from last time
            if lastcheck == "unavailable":
                lastcheck = "available"
                time.sleep(60)
                #print("going to text in stock")
                client.api.account.messages.create(
                to="+14125197470",
                from_="+13158609743",
                body="PS5 in stock at Target")
        else:
            #print("out of stock")
            ## send sms only when different from last time
            if lastcheck == "available":
                lastcheck = "unavailable"
                time.sleep(60)
                #print("going to text out of stock")
                client.api.account.messages.create(
                to="+14125197470",
                from_="+13158609743",
                body="PS5 no longer in stock at Target")
    except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError):
        continue
