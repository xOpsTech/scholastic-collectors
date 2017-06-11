from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
api = Api(app)
CORS(app)

import requests  # Set the request parameters

headers = {"Accept": "application/json"}  # Do the HTTP request
parser = reqparse.RequestParser()


class ApicaMetrcis(Resource):
    def post(self):
        data = request.get_json()
        print data
        return data, 200


api.add_resource(ApicaMetrcis, '/updates')
# api.add_resource(Incident, '/incidents/<duration>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
