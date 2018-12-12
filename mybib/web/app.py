from flask import Flask, request, jsonify
from mybib.neo4j import get_paper as get_paper_neo4j, insert_paper as insert_paper_neo4j, insert_reference, \
    get_reference as get_reference_neo4j, search_papers as search_papers_neo4j
from mybib.web.routing.regex_converters import PaperIdConverter
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import author, editor, journal, keyword, link, page_double_hyphen, doi

app = Flask(__name__)

app.url_map.converters['paper_id'] = PaperIdConverter


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

temporary_memory = {}


@app.route('/papers/<paper_id:identifier>', methods=['GET'])
def get_paper(identifier):
    return jsonify(get_paper_neo4j(identifier))


@app.route("/papers", methods=['POST'])
def post_paper():
    print(request.data.decode('utf-8'))
    bib_database = bibtexparser.loads(request.data.decode('utf-8'), parser=parser)
    [paper] = bib_database.entries

    insert_paper_neo4j(paper)

    response = jsonify()
    response.status_code = 201
    response.headers['location'] = '/papers/' + paper['ID']
    response.autocorrect_location_header = False
    return response


@app.route("/papers/search", methods=['GET'])
def search_papers():
    title = request.args['title']
    res = search_papers_neo4j(title)
    return jsonify(res)


@app.route('/references/<paper_id:referee>/<paper_id:referenced>', methods=['POST'])
def post_reference(referee, referenced):
    attr_dict = request.get_json()
    insert_reference(referee, referenced, attr_dict)

    response = jsonify()
    response.status_code = 201
    response.headers['location'] = f'/references/{referee}/{referenced}'
    response.autocorrect_location_header = False
    return response


@app.route('/references/<paper_id:referee>/<paper_id:referenced>', methods=['GET'])
def get_reference(referee, referenced):
    reference = get_reference_neo4j(referee, referenced)
    return jsonify(reference)
