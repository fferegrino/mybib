from flask import Blueprint, render_template

frontend = Blueprint('frontend', __name__)


@frontend.route('/admin', methods=['GET'])
def get_index():
    return render_template('admin.html')


@frontend.route('/', methods=['GET'])
def get_graph():
    return render_template('graph.html')
