from flask import Flask
from mybib.web.routing.regex_converters import PaperIdConverter
from mybib.web.api.papers import papers_api
from mybib.web.api.references import references_api

app = Flask(__name__)

app.url_map.converters['paper_id'] = PaperIdConverter
app.register_blueprint(papers_api)
app.register_blueprint(references_api)

