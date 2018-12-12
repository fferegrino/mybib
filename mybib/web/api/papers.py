from flask import Blueprint, request, jsonify
from mybib.neo4j import get_paper as get_paper_neo4j, insert_paper as insert_paper_neo4j, search_papers as search_papers_neo4j

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import author, editor, journal, keyword, link, page_double_hyphen, doi


def customizations(record):
    """Use some functions delivered by the library

    :param record: a record
    :returns: -- customized record
    """
    # record = type(record)
    record = author(record)
    record = editor(record)
    record = journal(record)
    record = keyword(record)
    record = link(record)
    record = page_double_hyphen(record)
    record = doi(record)
    return record


parser = BibTexParser()
parser.customization = customizations

papers_api = Blueprint('papers_api', __name__)


@papers_api.route('/api/papers/<paper_id:identifier>', methods=['GET'])
def get_paper(identifier):
    return jsonify(get_paper_neo4j(identifier))


@papers_api.route("/api/papers", methods=['POST'])
def post_paper():
    print(request.data.decode('utf-8'))
    bib_database = bibtexparser.loads(request.data.decode('utf-8'), parser=parser)
    [paper] = bib_database.entries

    insert_paper_neo4j(paper)

    response = jsonify()
    response.status_code = 201
    response.headers['location'] = '/api/papers/' + paper['ID']
    response.autocorrect_location_header = False
    return response


@papers_api.route("/api/papers/search", methods=['GET'])
def search_papers():
    title = request.args['title']
    res = search_papers_neo4j(title)
    return jsonify(res)
