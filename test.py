import argparse
import requests
import threading
import json
from flask import Flask, request
from utils import *
from os import getenv
from dotenv import load_dotenv

app = Flask(__name__)

"""
Script that sets up an endpoint and then sends to your node, and checks the response.

Use like this 'python test.py --endpoint http://yournodesendpoint
"""
env = load_dotenv(verbose=True)
rsa_private_key = getenv("RSA_PRIVATE_KEY")

parser = argparse.ArgumentParser()
parser.add_argument('--custom', '-c', action='store_true', default=False, help='Send your own custom Scenemark?')
parser.add_argument('--second-scenemark', '-ss', action='store_true', default=False, help='Send the second SceneMark')
parser.add_argument('--endpoint', '-e', help='Endpoint you want to send the SceneMark to.', required=True)
args = parser.parse_args()

HOST = '0.0.0.0'
PORT = '1337'
ENDPOINT = args.endpoint
CUSTOM = args.custom
SECOND_SCENEMARK = args.second_scenemark

def send_payload_to_node():
    print("\nLocal Node Test starting...")
    print(
        "\nSending a SceneMark your node",
        f"located at: {ENDPOINT} ..\n")

    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'}

    node_payload = generate_node_payload(
        f'http://{HOST}:{PORT}/test_sentry',
        1,
        rsa_private_key,
        CUSTOM,
        SECOND_SCENEMARK,
        'dummy-access-token'
        )

    with open("node_payload.json", 'w') as json_file:
        json.dump(node_payload, json_file)

    global scenemark_sent
    scenemark_sent = node_payload['SceneMark']

    requests.post(
        ENDPOINT,
        data=json.dumps(node_payload),
        headers=header,
        verify=False,
        stream=False)

@app.route("/test_sentry", methods=['POST'])
def test_sentry():

    scenemark = request.json

    print("> Request received back from your node: \n", json.dumps(scenemark, indent=3))

    with open("results/returned_scenemark.json", 'w') as json_file:
        json.dump(scenemark, json_file)

    print("\n...............................................................")
    print("\nChecking the returned SceneMark for various variables")
    print("\n1. Checking basic variables..")

    assert scenemark['SceneMarkID'] == scenemark_sent['SceneMarkID']
    print("SceneMarkID OK!")
    assert scenemark['TimeStamp'] == scenemark_sent['TimeStamp']
    print("TimeStamp OK!")

    previous_version_number = max([vc_item['VersionNumber'] for vc_item in scenemark_sent['VersionControl']['VersionList']])
    new_version_number = max([vc_item['VersionNumber'] for vc_item in scenemark['VersionControl']['VersionList']])
    assert new_version_number == previous_version_number + 1.0
    print("VersionControl OK!")

    #Check the analysis list parts
    print("\n2. Checking the AnalysisList update doing by the Node")
    for index, analysis_list_item in enumerate(scenemark['AnalysisList']):
        if analysis_list_item['VersionNumber'] == new_version_number:
            #ali means analysis_list_item
            ali = scenemark['AnalysisList'][index]

    print("Checking for errors")
    if ali['ProcessingStatus'] == 'Error' or ali['ProcessingStatus'] == 'Failed':
        print("The Node ran into an error..\n")
        if ali['ErrorMessage']:
            print("The Error Message reads:", ali['ErrorMessage'])
        else:
            print("but a precise error message is missing.")
    else:
        print("No errors in the returned SceneMark")

    print("This is what your node added to the SceneMark:")
    print(json.dumps(ali, indent = 3))

    print("\n...............................................................")
    print("Tests passed! Ctrl + c to kill the test")
    print("This script is under construction. More serious testing will be added.")

@app.route("/")
def up():
    return "I am up!"

@app.before_first_request
def activate_job():
    def run_job():
        send_payload_to_node()
    thread = threading.Thread(target=run_job)
    thread.start()

if __name__ == "__main__":
    start_runner(HOST, PORT)
    app.run(
        host = HOST,
        port = PORT
    )
