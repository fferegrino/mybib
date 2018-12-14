from flask import Blueprint, request, jsonify
from mybib.neo4j import recent_papers_and_references

root_api = Blueprint('root_api', __name__)


@root_api.route('/api/recent')
def get_recent_nodes():
    nodes, references = recent_papers_and_references()
    return jsonify({
        'nodes': nodes,
        'references': references
    })
