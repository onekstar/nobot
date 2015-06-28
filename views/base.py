#!/usr/bin/env python
# encoding: utf-8

from flask import jsonify, request

def _get_page_info():
    page = request.args.get("page")
    if not (page and page.isdigit()):
        page = 1
    else:
        page = int(page)

    pagesize = request.args.get("pagesize")
    if not (pagesize and pagesize.isdigit()):
        pagesize = 10
    else:
        pagesize = int(pagesize)

    return page, pagesize

def api_response(code=0, data=None, message=None):
    """
    构造api的json返回值
    """
    rst_dict = {
        'code': code,
        'message': message or '',
        'data': data or ''
    }
    return jsonify(rst_dict)
