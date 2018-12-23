from flask import Flask
from flask_graphql import GraphQLView

from mybib.graphql import schemas
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
app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql', schema=schemas.schema, graphiql=True)
)
