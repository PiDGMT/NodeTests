import argparse
import json
import requests
from data_generator import generate_scenemark
parser = argparse.ArgumentParser()

#Load the Node's URI
parser.add_argument('--custom', '-c', action='store_true', default=False, help='Send your own custom Scenemark?')
parser.add_argument('--endpoint', '-e', help='Endpoint you want to send the SceneMark to.')
args = parser.parse_args()

endpoint = ""
scenemark = generate_scenemark(args.custom)



print("Sending a SceneMark your node..")
answer = requests.post(
            endpoint,
            data=json.dumps(scenemark),
            #headers=?,
            verify=False,
            stream=False).json()

# Do stuff with the answer
try:
    with open("response/SceneMark.json", 'w') as json_file:
        json.dump(answer, json_file)
except:
    print("Response not a json.")



