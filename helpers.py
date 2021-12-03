import json
from random import choice
import datetime

# #We want to load the file as a json, change the accesstoken, and then dump it as a raw text to be able to send it
def payload(json_sm_or_sd):
    with open(json_sm_or_sd) as json_file:
        payload = json.load(json_file)
    return json.dumps(payload)

def load_json(js0n):
    with open(js0n) as json_file:
        return json.load(json_file)

def generate_random_id(length):
    return ''.join([choice('0123456789abcdef') for n in range(length)])

# Helper Functions
def get_current_utc_timestamp():
    return f"{'{:%Y-%m-%dT%H:%M:%S.%f}'.format(datetime.datetime.utcnow())[:-3]}Z"