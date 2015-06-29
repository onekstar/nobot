# encoding:utf-8
from datetime import datetime
from StringIO import StringIO
from urllib import quote

from flask import request, Blueprint, g, current_app, abort, Response, render_template

from views.base import api_response, _get_page_info

from dao.novel import NovelDAO

from tasks.novel import sync as sync_task
from tasks.novel import sync_chapters_content


bp_novel = Blueprint('novel', __name__)

@bp_novel.route('/api/novel/add', methods=['POST'])
def add():
    """
    新增Novel
    """
    name, rule = map(request.form.get, ('name', 'rule'))
    if not all([name, rule]):
        return api_response(code=400, message=u'参数缺失')

    novel_dao = NovelDAO(g.db, current_app.logger)
    result, obj = novel_dao.add(name, rule)
    if not result:
        return api_response(code=500, message=obj)
    
    return api_response(code=0, data=obj.to_dict())

    
@bp_novel.route('/api/novel/sync', methods=['POST'])
def sync():
    """
    发起同步
    """
    id = request.form.get('id', int)
    async_result = sync_task.apply_async((id, ))
    return api_response(code=0, data={'task_id': async_result.id, 'state': async_result.state})

@bp_novel.route('/api/novel/content/sync', methods=['POST'])
def sync_content():
    """
    发起章节内容同步
    """
    id = request.form.get('id', int)
    async_result = sync_chapters_content.apply_async((id, ))
    return api_response(code=0, data={'task_id': async_result.id, 'state': async_result.state})

@bp_novel.route('/api/novel/download', methods=['GET'])
def download():
    """
    下载小说
    """
    id = request.args.get('id', int)

    novel_dao = NovelDAO(g.db, current_app.logger)
    novel = novel_dao.get_by_id(id)

    if not novel:
        abort(404)

    stream = StringIO()
    for content in novel_dao.get_contents(novel):
        stream.write(content.encode('utf-8'))
        stream.write('\n')
        
    content_length = stream.tell()
    stream.seek(0)
    resp = Response(stream)
    resp.headers.set("Content-Disposition", "attachment", filename=quote((novel.name + '.txt').encode('utf-8')))
    resp.headers.set("Content-Length", content_length)
    resp.headers.set("Content-Type", "application/octet-stream")

    return resp

@bp_novel.route('/api/novel/chapter/list', methods=['GET'])
def get_chapter_list():
    """
    获取章节列表
    """
    page, pagesize = _get_page_info()
    id = request.args.get('id', int)

    novel_dao = NovelDAO(g.db, current_app.logger)
    count, chapter_list = novel_dao.get_chapter_list(id, page=page, pagesize=pagesize)

    c_list = [{
        'id': c.id,
        'title': c.title, 
        'publish_time': datetime.strftime(c.publish_time, '%Y-%m-%d %H:%M')
    } for c in chapter_list]

    return api_response(code=0, data={'count': count, 'list': c_list})

@bp_novel.route('/api/novel/search', methods=['GET'])
def search_novel():
    keyword = request.args.get('keyword', '')
    if not keyword:
        return api_response(code=400, message=u'参数缺失')
    novel_dao = NovelDAO(g.db, current_app.logger)
    novels = novel_dao.search_novel(keyword)
    novels = [novel.to_dict() for novel in novels]
    return api_response(code=0, data=novels)

@bp_novel.route('/novel/create', methods=['GET'])
def get_craete_page():
    """
    获取创建页面
    """
    return render_template('novel-create.html')
