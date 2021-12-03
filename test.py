import argparse
import requests
import threading
import json
import time
from flask import Flask, request
from data_generator import generate_node_payload

app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--custom', '-c', action='store_true', default=False, help='Send your own custom Scenemark?')
parser.add_argument('--endpoint', '-e', help='Endpoint you want to send the SceneMark to.', required=True)
args = parser.parse_args()

HOST = '127.0.0.1'
PORT = '4444'
ENDPOINT = args.endpoint
CUSTOM = args.custom

def send_payload_to_node():
    print("TESTSCRIPT")
    print(
        "\nSending a SceneMark your node",
        f"located at: {ENDPOINT} ..\n")

    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'}

    node_payload = generate_node_payload(
        f'http://{HOST}:{PORT}/test_sentry',
        CUSTOM,
        'dummy-access-token'
        )

    answer = requests.post(
        ENDPOINT,
        data=json.dumps(node_payload),
        headers=header,
        verify=False,
        stream=False)

@app.before_first_request
def activate_job():
    def run_job():
        send_payload_to_node()
    thread = threading.Thread(target=run_job)
    thread.start()

@app.route("/test_sentry", methods=['POST'])
def test_sentry():
    print("> Request received back from your node: ", request.json)
    with open("result.json", 'w') as json_file:
        json.dump(request.json, json_file)
    scenemark = request.json
    assert scenemark['SceneMarkID'] == "SMK_00000000-0000-0000-0000-000000000000_0001_123456"
    return "Success!"

@app.route("/")
def up():
    return "I am up!"

def start_runner():
    def start_loop():
        not_started = True
        while not_started:
            print('In start loop')
            try:
                r = requests.get(f'http://{HOST}:{PORT}/')
                if r.status_code == 200:
                    print(f"\nServer started: response code {r.status_code}.",
                            "Quiting start_loop\n")
                    not_started = False
            except:
                print('Server not yet started')
            time.sleep(2)

    print('Started runner')
    thread = threading.Thread(target=start_loop)
    thread.start()

if __name__ == "__main__":
    start_runner()
    app.run(
        host = HOST,
        port = PORT
    )
