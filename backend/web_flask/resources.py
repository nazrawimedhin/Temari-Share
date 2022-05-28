from . import bp
from flask import render_template
from models import Resource


@bp.route('/')
def index():
    resources = Resource.query.all()
    render_template("index.html", resources=resources)


@bp.route('/<int:res_id>')
def get_resource(res_id):
    resource = Resource.query.filter(Resource.id == res_id).first_or_404()
    render_template("resource.html", resource=resource)
