import helpers

def generate_scenemark(custom):
    sm = helpers.load_json('payloads/scenemark.json')
    if custom:
        sm = helpers.load_json('payloads/custom_scenemark.json')
    timestamp = helpers.get_current_utc_timestamp()
    sm['TimeStamp'] = timestamp
    return sm

def generate_nodesequencer_address(
    endpoint,
    token
    ):
    ns_address = {}
    ns_address['Ingress'] = endpoint
    ns_address['Token'] = token
    return ns_address

def generate_node_payload(
    endpoint,
    custom_scenemark = False,
    token = "dummy-access-token"
    ):
    node_load = {}
    node_load['SceneMark'] = generate_scenemark(custom_scenemark)
    node_load['NodeSequencerAddress'] = generate_nodesequencer_address(endpoint, token)
    return node_load



