import os

from flask import Flask, json, abort, request, send_from_directory
from flask_cors import CORS


app = Flask(__name__, static_folder='webapp/build/')
CORS(app)

COLLECTION_MODE_ZONE = 0
COLLECTION_MODE_DISABLED = 1
COLLECTION_MODE_ALL = 2

API_URI = '/api/'
ZONE_URI = API_URI + 'zone'
COLLECTION_URI = API_URI + 'collection'
COLLECTION_MODE_URI = API_URI + 'collection_mode'

zone = 1
collection = 0
collection_mode = COLLECTION_MODE_ZONE


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if not path:
        path = "index.html"

    if path_to_file_exists(path):
        return send_from_directory(app.static_folder, path)
    else:
        return abort(404)


def path_to_file_exists(path):
    if not path:
        return False

    full_path = app.static_folder + "/" + path
    print(full_path)

    return os.path.exists(full_path)

@app.route(ZONE_URI, methods=['GET', 'POST'])
def handle_zone():
    global zone
    if is_post(request):
        zone = request.json['zone']
    return json.dumps(zone)


@app.route(COLLECTION_URI, methods=['GET', 'POST'])
def handle_collection():
    global collection
    if is_post(request):
        collection = request.json['collection']
    return json.dumps(collection)


@app.route(COLLECTION_MODE_URI, methods=['GET', 'POST'])
def handle_mode():
    global collection_mode
    if is_post(request):
        collection_mode = request.json['collectionMode']
    return json.dumps(collection_mode)


def is_post(req):
    return req.method == 'POST'


if __name__ == '__main__':
    app.run()
