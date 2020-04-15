#!/usr/bin/env python
import configparser
import json
import requests
import csv
import os
from datetime import datetime

# pull in data from config file
config = configparser.ConfigParser()
config.read('config.ini')

# Build headers and URI for web request
headers = { 'Content-Type': 'application/json',
            'X-Auth-Token': config['creds']['token'],   
            'X-User-Id': config['creds']['uid']}

uri = config['other']['rchost'] + 'api/v1/groups.members?roomName=' + config['other']['room']

# check if we need to use self signed certs and set values appropriately
if (config['other']['verifycert'] == "False"):
    requests.packages.urllib3.disable_warnings()
    verify = False
else:
    verify = True

# load json web request into a dict
# note set verifycert to 0 to ignore self signed/invalid certs
response = requests.get(uri, headers=headers, verify=verify)
response_parsed = json.loads(response.content)

# This is for testing. Read json in from a file instead of the web.
with open('roomusers_a25.json', 'r') as f:
    response_parsed = json.load(f)

# select just "members" from web request response
users = response_parsed['members']


# Output to file section
filename = "status_" + str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day) + ".csv"
# clean up if today's report already exists
if os.path.exists(filename):
  os.remove(filename)
# Open a CSV and loop through users
with open(filename, 'w', newline='') as csvfile:
    userinfo = csv.writer(csvfile, dialect='excel')
    userinfo.writerow(['Name', 'Current Login Status', 'Daily Status'])
    for user in users:
        # note special handling for users with no statusText
        writeStatus = False
        if 'statusText' in user.keys():
            if user['statusText'] != '':
                writeStatus = True
        if writeStatus:
            userinfo.writerow([user['name'], user['status'], user['statusText']])                
        else:
            userinfo.writerow([user['name'], user['status'], "location unknown"])
