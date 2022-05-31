from flask import Blueprint, render_template
from models import Resource


bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    all_resources = Resource.query.all()
    return render_template('index.html', resources=all_resources)


@bp.route('/home')
def home():
    all_resources = Resource.query.all()
    return render_template('home.html', resources=all_resources)
