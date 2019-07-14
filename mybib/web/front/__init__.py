from flask import Blueprint, render_template, request
from werkzeug.utils import redirect

from mybib.neo4j.models import Keyword, Paper, Project

frontend = Blueprint("frontend", __name__)


@frontend.route("/admin", methods=["GET"])
def get_index():
    return render_template("admin.html")


@frontend.route("/", methods=["GET"])
def get_graph():
    return render_template("graph.html")


@frontend.route("/papers/<paper_id:identifier>", methods=["GET"])
def get_paper(identifier):
    paper = Paper(ID=identifier).fetch()

    keywords = ",".join([kw["value"] for kw in paper.fetch_keywords()])
    projects = ",".join([pr["name"] for pr in paper.fetch_projects()])

    paper = paper.asdict()
    title = paper.pop("title")
    time = paper.pop("_time")
    ID = paper.pop("ID")
    bibtex = paper.pop("_bibtex")
    return render_template(
        "paper.html",
        ID=ID,
        keywords=keywords,
        projects=projects,
        title=title,
        paper=paper,
    )


@frontend.route("/papers/<paper_id:identifier>", methods=["POST"])
def post_paper(identifier):
    updated_paper = request.form.to_dict()

    new_keywords = set(updated_paper.pop("keywords").split(","))
    new_projects = set(updated_paper.pop("projects").split(","))
    ID = updated_paper.pop("ID")

    paper_to_update = Paper(ID=ID).fetch()
    existing_keywords = {
        keyword["value"] for keyword in paper_to_update.fetch_keywords()
    }
    existing_projects = {
        project["name"] for project in paper_to_update.fetch_projects()
    }

    keep_keywords = existing_keywords.intersection(new_keywords)
    to_remove_keywords = existing_keywords - keep_keywords
    to_add_keywords = new_keywords - keep_keywords

    keep_projects = existing_projects.intersection(new_projects)
    to_remove_projects = existing_projects - keep_projects
    to_add_projects = new_projects - keep_projects

    for kw in to_add_keywords:
        keyword = Keyword(value=kw)
        fetched_keyword = keyword.fetch()
        if fetched_keyword:
            paper_to_update.keywords.add(fetched_keyword)
        else:
            keyword.save()
            paper_to_update.keywords.add(keyword)

    for kw in to_remove_keywords:
        keyword = Keyword(value=kw)
        fetched_keyword = keyword.fetch()
        paper_to_update.keywords.remove(fetched_keyword)

    for pj in to_add_projects:
        project = Project(name=pj)
        fetched_project = project.fetch()
        if fetched_project:
            paper_to_update.projects.add(fetched_project)
        else:
            project.save()
            paper_to_update.projects.add(project)

    for pj in to_remove_projects:
        project = Project(name=pj)
        fetched_project = project.fetch()
        paper_to_update.projects.remove(fetched_project)

    paper_to_update.save()

    return redirect("/papers/" + identifier)
