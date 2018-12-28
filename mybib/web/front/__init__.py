from flask import Blueprint, render_template, request

from mybib.neo4j.models import Paper

frontend = Blueprint('frontend', __name__)


@frontend.route('/admin', methods=['GET'])
def get_index():
    return render_template('admin.html')


@frontend.route('/', methods=['GET'])
def get_graph():
    return render_template('graph.html')


@frontend.route('/papers/<paper_id:identifier>', methods=['GET'])
def get_paper(identifier):
    paper = Paper(ID=identifier).fetch()

    keywords = ','.join([kw['value'] for kw in paper.fetch_keywords()])
    projects = ','.join([pr['name'] for pr in paper.fetch_projects()])

    paper = paper.asdict()
    title = paper.pop('title')
    time = paper.pop('_time')
    ID = paper.pop('ID')
    bibtex = paper.pop('_bibtex')
    return render_template('paper.html',
                           ID=ID,
                           keywords=keywords,
                           projects=projects,
                           title=title, paper=paper)


@frontend.route('/papers/<paper_id:identifier>', methods=['POST'])
def post_paper(identifier):
    updated_paper = request.form.to_dict()
    keywords = updated_paper.pop('keywords').split('')
    projects = updated_paper.pop('projects')
    return str(request.form.to_dict())
