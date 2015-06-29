# encoding:utf-8
from flask import request, Blueprint, g, current_app, abort, Response, render_template

bp_index = Blueprint('index', __name__)

@bp_index.route('/', methods=['GET'])
def index():
    return render_template('index.html')
