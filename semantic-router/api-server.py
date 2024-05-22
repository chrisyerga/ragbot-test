# api-server.py
import os
import sys
from semantic_router.layer import RouteLayer
from semantic_router.encoders import OpenAIEncoder
from semantic_router import Route
from flask import Flask, jsonify
from flask import request

app = Flask(__name__)

@app.route('/process_text', methods=['POST'])
def process_text():
    text = request.json['text']  # Get text from JS request
    processed_text = process_paragraph(text)  # Call Python function
    return jsonify({'result': processed_text})  # Return result to JS


indexes = ['chitchat', 'politics', 'recovery-my']
routes = None
encoder = None
rl = None

def initialize():
    global routes
    global encoder
    global rl

    try:
        # or for OpenAI
        os.environ["OPENAI_API_KEY"] = sys.argv[1]
        key = sys.argv[1]
        print(f"APIKEY={key if key != None else '<missing>'}")
        encoder = OpenAIEncoder()
        routes = get_routes()
        rl = RouteLayer(encoder=encoder, routes=routes)
    except Exception  as err:
        raise err


@app.route('/semanticroute', methods=['GET'])
def getSemanticRoute():
    text = request.args['text']
    print(f"request:{text if text != None else '<none>'}")
    print(f"routes:{routes if routes != None else '<none>'}")
    print(f"encoder:{encoder if encoder != None else '<none>'}")
    print(f"rl:{rl if rl != None else '<none>'}")
    result = rl(text).name
    return jsonify({'result': result})


def getIndexFile(file_name: str):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Open the PDF file in read-binary mode
    with open(f'{current_dir}/routes/{file_name}.txt', 'rb') as index_file:
        return [line for line in index_file.read().splitlines() if len(line)>0]

def init_routes(index):
    return Route(
    name=index,
    utterances=getIndexFile(index),
    )

def get_routes():
    try:
        return [init_routes(index) for index in indexes]
    except Exception  as err:
        raise err


if __name__ == '__main__':
    initialize()
    app.run()