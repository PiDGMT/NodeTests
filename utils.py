import json
from random import choice
import datetime
import threading
import time
import requests
import jwt
import uuid

def generate_scenemark(custom):
    sm = load_json('payloads/scenemark.json')
    if custom:
        sm = load_json('payloads/custom_scenemark.json')
    timestamp = get_current_utc_timestamp()
    sm['TimeStamp'] = timestamp
    return sm

def generate_nodesequencer_header(
    endpoint,
    token,
    datatype,
    rsa_private_key,
    ):
    ns_header = {}
    ns_header['Ingress'] = endpoint
    ns_header['Token'] = token
    ns_header['NodeToken'] = generate_node_token(rsa_private_key)
    node_input = {}
    node_input['DataTypeMode'] = datatype
    ns_header['NodeInput'] = node_input
    return ns_header

def generate_node_payload(
    endpoint,
    datatype,
    rsa_private_key,
    custom_scenemark = False,
    token = "dummy-access-token"
    ):
    node_load = {}
    node_load['SceneMark'] = generate_scenemark(custom_scenemark)
    node_load['NodeSequencerHeader'] = generate_nodesequencer_header(endpoint, token, datatype, rsa_private_key)
    return node_load

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

def generate_node_token(rsa_private_key, issuer = "Scenera-DataPipeline", audience = "Scenera-Node"):
    # Generate the JWT that we need to generate to call the node.
    now = int(datetime.datetime.utcnow().timestamp())
    expires = int((datetime.datetime.utcnow() + datetime.timedelta(hours=100)).timestamp())
    payload = {
        "iat": now,
        "jti": str(uuid.uuid4()),
        "Sender": "NodeSequencer",
        "Company": "Scenera",
        "nbf": now,
        "exp": expires,
        "iss": issuer,
        "aud": audience,
    }
    begin = "-----BEGIN RSA PUBLIC KEY-----\n"
    end = "\n-----END RSA PUBLIC KEY-----"
    pkey = begin + rsa_private_key + end
    token = jwt.encode(payload, pkey, algorithm='RS256')
    return token

def start_runner(host,port):
    def start_loop():
        not_started = True
        while not_started:
            try:
                r = requests.get(f'http://{host}:{port}/')
                if r.status_code == 200:
                    not_started = False
            except:
                print('Server not yet started')
            time.sleep(2)

    thread = threading.Thread(target=start_loop)
    thread.start()