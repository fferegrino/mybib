from flask import Blueprint, request, jsonify

from mybib.neo4j.models import Paper
from mybib.web.authentication import requires_auth

references_api = Blueprint('references_api', __name__)


@references_api.route('/api/references/<paper_id:referee>/<paper_id:referenced>', methods=['POST'])
@requires_auth
def post_reference(referee, referenced):
    attr_dict = request.get_json()

    referee_paper = Paper(ID=referee).fetch()
    referenced_paper = Paper(ID=referenced).fetch()

    referee_paper.references.add(referenced_paper, attr_dict)
    referee_paper.save()

    response = jsonify()
    response.status_code = 201
    response.headers['location'] = f'/api/references/{referee}/{referenced}'
    response.autocorrect_location_header = False
    return response


@references_api.route('/api/references/<paper_id:referee>/<paper_id:referenced>', methods=['GET'])
def get_reference(referee, referenced):
    reference = None  # get_reference_neo4j(referee, referenced)
    return jsonify(reference)
