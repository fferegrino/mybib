from flask import Blueprint, request, jsonify
from mybib.web.authentication import requires_auth

references_api = Blueprint('references_api', __name__)


@references_api.route('/api/references/<paper_id:referee>/<paper_id:referenced>', methods=['POST'])
@requires_auth
def post_reference(referee, referenced):
    attr_dict = request.get_json()
    #insert_reference(referee, referenced, attr_dict)

    response = jsonify()
    response.status_code = 201
    response.headers['location'] = f'/api/references/{referee}/{referenced}'
    response.autocorrect_location_header = False
    return response


@references_api.route('/api/references/<paper_id:referee>/<paper_id:referenced>', methods=['GET'])
def get_reference(referee, referenced):
    reference = None #get_reference_neo4j(referee, referenced)
    return jsonify(reference)
