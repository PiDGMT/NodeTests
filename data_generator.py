import helpers

def generate_scenemark(custom):
    sm = helpers.load_json('payloads/scenemark.json')
    if custom:
        sm = helpers.load_json('payloads/custom_scenemark.json')
    timestamp = helpers.get_current_utc_timestamp()
    sm['TimeStamp'] = timestamp
    return sm

def generate_nodesequencer_header(
    endpoint,
    token,
    datatype
    ):
    ns_header = {}
    ns_header['Ingress'] = endpoint
    ns_header['Token'] = token
    node_input = {}
    node_input['DataTypeMode'] = datatype
    ns_header['NodeInput'] = node_input
    return ns_header

def generate_node_payload(
    endpoint,
    datatype,
    custom_scenemark = False,
    token = "dummy-access-token"
    ):
    node_load = {}
    node_load['SceneMark'] = generate_scenemark(custom_scenemark)
    node_load['NodeSequencerHeader'] = generate_nodesequencer_header(endpoint, token, datatype)
    return node_load



