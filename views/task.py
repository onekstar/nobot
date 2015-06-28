# encoding:utf-8
from flask import request, Blueprint, g, current_app

from views.base import api_response

from tasks.celery import app as celery_app

bp_task = Blueprint('task', __name__)

@bp_task.route('/api/task/state', methods=['GET'])
def get_state():
    """
    查看任务状态
    """
    id = request.args.get('id')
    if not id:
        return api_response(code=400, message=u'参数缺失')

    task = celery_app.AsyncResult(id)
    return api_response(code=0, data={'state': task.state, 'info': task.info})
