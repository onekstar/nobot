#coding:utf-8
import json
import uuid

def pprint(data):
    print json.dumps(data, encoding='utf-8', ensure_ascii=False, indent=4) 
