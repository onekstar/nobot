# encoding:utf-8
from flask import request, Blueprint, g, current_app, abort, Response

from views.base import api_response, _get_page_info

from dao.chapter import ChapterDAO


bp_chapter = Blueprint('chapter', __name__)

@bp_chapter.route('/api/chapter/read', methods=['GET'])
def read():
    """
    在线阅读
    """
    id, novel_id = map(request.args.get, ('id', 'novel_id'))
    if not (id or novel_id):
        return api_response(code=400, message=u'参数缺失')

    chapter_dao = ChapterDAO(g.db, current_app.logger)
    pre, current, next_ = chapter_dao.read(id, novel_id)

    data = {
        'pre': pre,
        'next': next_,
        'content': current and current.to_dict()
    }

    return api_response(code=0, data=data)
