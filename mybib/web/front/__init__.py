from flask import Blueprint, render_template

frontend = Blueprint('frontend', __name__)


@frontend.route('/', methods=['GET'])
def get_index():
    return render_template('index.html')


@frontend.route('/graph', methods=['GET'])
def get_graph():
    return render_template('graph.html')
