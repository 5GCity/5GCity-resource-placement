# Copyright (C) 2019 - Virtual Open Systems SAS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#   author          =   Teodora Sechkova
#   author_email    =   teodora@virtualopensystems.com

from flask import Flask, jsonify
from flask import request as request
from flask import make_response, abort
import flask_restplus
import jsonref
from bjointsp.heuristic import placement
from bjointsp.read_write import store

app = Flask(__name__)
api = flask_restplus.Api(app)


name_space = api.namespace('placement', description='Main APIs')
with open("parameters/5gcity/input_schema") as in_schema:
    in_model = api.schema_model('Input', jsonref.load(in_schema))

with open("parameters/5gcity/out_schema") as out_schema:
    out_model = api.schema_model('Output', jsonref.load(out_schema))


@name_space.route("/<path:placement_id>")
class PlacementResponse(flask_restplus.Resource):

    @api.doc(params={'placement_id': 'An ID of the placement operation'})
    @api.response(404, 'Not Found')
    @api.response(200, 'Success', out_model)
    def get(self, placement_id):
        try:
            result = store.get_placement_result(placement_id)

            if result is None:
                return 'Placement result not found', 404

            return result, 200
        except Exception as err:
            return err, 500


@name_space.route("")
class PlacementRequest(flask_restplus.Resource):

    @api.response(404, 'Not Found')
    @api.response(200, 'Success', out_model)
    def get(self):
        result = store.get_placement_db()

        if result is None:
            return 'Placement requests DB is empty', 404
        return result, 200

    @api.doc(responses={201: 'Created'})
    @api.doc(body=in_model)
    def post(self):
        try:
            if not request.json:
                abort(400)

            result = placement.place(request.json['network'], request.json['fwchain'], request.json['fwchain']['source'],
                           fixed_file=None, prev_embedding_file=None, cpu=None, mem=None, dr=50)
        except Exception as err:
            return err, 500
        else:
            return {'placement_id': str(result)}, 201
