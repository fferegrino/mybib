from flask import Flask

from mybib.web.api.papers import papers_api
from mybib.web.api.references import references_api
from mybib.web.api.root import root_api
from mybib.web.front import frontend
from mybib.web.routing.regex_converters import PaperIdConverter

app = Flask(__name__, template_folder='front/templates', static_folder='front/static')

app.url_map.converters['paper_id'] = PaperIdConverter
app.register_blueprint(frontend)
app.register_blueprint(root_api)
app.register_blueprint(papers_api)
app.register_blueprint(references_api)

if __name__ == '__main__':
    app.run()
