from flask import Blueprint

gehalt_api = Blueprint('gehalt_api', __name__)

@gehalt_api.route("/list")
def list():
    return "list of ..."