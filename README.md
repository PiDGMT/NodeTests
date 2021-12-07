# Testing Suite to test AI Nodes

Testing scripts to use the nodes. Sets up a Flask endpoint to figure as a Mock NodeSequencer. Then sends a payload to your node, and checks whether it gets a proper response.

Run like so:

> python test.py -e http://theendpointof.your/node

Use flag -c if you want to send the custom SceneMark, which you can change yourself in the payloads folder

The current script is usable but the Test is still mainly under construction
