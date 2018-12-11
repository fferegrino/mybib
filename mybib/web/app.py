from flask import Flask, request, jsonify
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import author, editor, journal, keyword, link, page_double_hyphen, doi

app = Flask(__name__)


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


@app.route('/papers/<identifier>', methods=['GET'])
def get_paper(identifier):
    return str(temporary_memory[identifier])


@app.route("/papers", methods=['POST'])
def post_papers():
    print(request.data.decode('utf-8'))
    bib_database = bibtexparser.loads(request.data.decode('utf-8'), parser=parser)
    [paper] = bib_database.entries

    temporary_memory[paper['ID']] = paper

    response = jsonify()
    response.status_code = 201
    response.headers['location'] = '/papers/' + paper['ID']
    response.autocorrect_location_header = False
    return response
