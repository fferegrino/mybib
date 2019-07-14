from flask import Blueprint, jsonify, request

root_api = Blueprint("root_api", __name__)


@root_api.route("/api/recent")
def get_recent_nodes():
    # nodes, references = recent_papers_and_references()
    return jsonify({"nodes": None, "references": None})
