from flask import Flask, json, request
from flask_cors import CORS

api = Flask(__name__)
CORS(api)

COLLECTION_MODE_ZONE = 0
COLLECTION_MODE_DISABLED = 1
COLLECTION_MODE_ALL = 2

BASE_URI = '/api/'
ZONE_URI = BASE_URI + 'zone'
COLLECTION_URI = BASE_URI + 'collection'
COLLECTION_MODE_URI = BASE_URI + 'collection_mode'

zone = 1
collection = 0
collection_mode = COLLECTION_MODE_ZONE


@api.route(ZONE_URI, methods=['GET', 'POST'])
def handle_zone():
    global zone
    if is_post(request):
        zone = request.json['zone']
    return json.dumps(zone)


@api.route(COLLECTION_URI, methods=['GET', 'POST'])
def handle_collection():
    global collection
    if is_post(request):
        collection = request.json['collection']
    return json.dumps(collection)


@api.route(COLLECTION_MODE_URI, methods=['GET', 'POST'])
def handle_mode():
    global collection_mode
    if is_post(request):
        collection_mode = request.json['collectionMode']
    return json.dumps(collection_mode)


def is_post(req):
    return req.method == 'POST'


if __name__ == '__main__':
    api.run()
