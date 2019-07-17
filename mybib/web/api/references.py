from flask import Blueprint, jsonify, request

from mybib.graphql.access_layer import EntityAlreadyExistsError, insert_reference
from mybib.web.authentication import requires_auth

references_api = Blueprint("references_api", __name__)


@references_api.route(
    "/api/references/<paper_id:referee>/<paper_id:referenced>", methods=["POST"]
)
@requires_auth
def post_reference(referee, referenced):
    attr_dict = request.get_json()
    response = jsonify()

    try:
        insert_reference(referee, referenced, attr_dict)
        response.status_code = 201
        response.headers["location"] = f"/api/references/{referee}/{referenced}"
        response.autocorrect_location_header = False
    except AssertionError:
        response.status_code = 400
    except EntityAlreadyExistsError as ae:
        response.status_code = 409
        response.headers["location"] = f"/api/references/{referee}/{referenced}"

    return response
