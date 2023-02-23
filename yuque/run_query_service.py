# utf-8
import datetime

import json
import logging

from yuque import yuque_service

##
# for test
##

FORMAT = '%(asctime)s ' \
         '%(levelname)s ' \
         '[%(threadName)s--%(thread)d] ' \
         '%(message)s'
logging.basicConfig(format=FORMAT, level="DEBUG")
logger = logging.getLogger('yuque_service')


def run_catalog_node_list():
    lib_id_list = [6905092, 6905122, 20978116, 20684276, 24750617, 27780490, 32207768]
    catalog_node_list = yuque_service.get_catalog_node_list(6905122)
    logger.info("catalog_node_dict:%s", json.dumps(catalog_node_list))


def run_catalog_node_convert():
    catalog_node_list_json = '[{"type":"DOC","title":"目录demo","uuid":"3Vre0DgSaelyeb7M","url":"ibngpn05klpaxw9u","prev_uuid":null,"sibling_uuid":"VmgeZPUMRSR-T4SY","child_uuid":"Y_y6WtJ_ka_joLf6","parent_uuid":null,"doc_id":115027221,"level":0,"id":115027221,"open_window":1,"visible":1},{"type":"DOC","title":"AA","uuid":"Y_y6WtJ_ka_joLf6","url":"pl9eg6izu8mtglp9","prev_uuid":"3Vre0DgSaelyeb7M","sibling_uuid":"rhHYd3cZ7pxEYAM8","child_uuid":null,"parent_uuid":"3Vre0DgSaelyeb7M","doc_id":115027710,"level":1,"id":115027710,"open_window":1,"visible":1},{"type":"DOC","title":"A","uuid":"rhHYd3cZ7pxEYAM8","url":"otrcevskgdaya3k9","prev_uuid":"Y_y6WtJ_ka_joLf6","sibling_uuid":"aFAiU6LGPhvJ6Wf-","child_uuid":null,"parent_uuid":"3Vre0DgSaelyeb7M","doc_id":115027439,"level":1,"id":115027439,"open_window":1,"visible":1},{"type":"DOC","title":"AAA","uuid":"aFAiU6LGPhvJ6Wf-","url":"fv7yd4y4176xuoo9","prev_uuid":"rhHYd3cZ7pxEYAM8","sibling_uuid":null,"child_uuid":"zWN0s5pwDG0GkJfC","parent_uuid":"3Vre0DgSaelyeb7M","doc_id":115027264,"level":1,"id":115027264,"open_window":1,"visible":1},{"type":"DOC","title":"B","uuid":"zWN0s5pwDG0GkJfC","url":"bzlf8qln5im4t64e","prev_uuid":"aFAiU6LGPhvJ6Wf-","sibling_uuid":null,"child_uuid":null,"parent_uuid":"aFAiU6LGPhvJ6Wf-","doc_id":115027408,"level":2,"id":115027408,"open_window":1,"visible":1},{"type":"DOC","title":"有氧运动与无氧运动","uuid":"VmgeZPUMRSR-T4SY","url":"ggga9k","prev_uuid":"3Vre0DgSaelyeb7M","sibling_uuid":"qaegYck0ZG_lw5Tb","child_uuid":null,"parent_uuid":null,"doc_id":83800025,"level":0,"id":83800025,"open_window":1,"visible":1},{"type":"TITLE","title":"Finance","uuid":"qaegYck0ZG_lw5Tb","url":null,"prev_uuid":"VmgeZPUMRSR-T4SY","sibling_uuid":"bna1nP6Jujruc0b_","child_uuid":"5IBftcbxQE7EVrnd","parent_uuid":null,"doc_id":null,"level":0,"id":null,"open_window":1,"visible":1},{"type":"DOC","title":"Real estate","uuid":"5IBftcbxQE7EVrnd","url":"fexi9y","prev_uuid":"qaegYck0ZG_lw5Tb","sibling_uuid":null,"child_uuid":null,"parent_uuid":"qaegYck0ZG_lw5Tb","doc_id":76896112,"level":1,"id":76896112,"open_window":0,"visible":1},{"type":"TITLE","title":"Demo","uuid":"bna1nP6Jujruc0b_","url":null,"prev_uuid":"qaegYck0ZG_lw5Tb","sibling_uuid":"wfNAXnRxNzFjGbzP","child_uuid":"6905122:JHVTnwu3BB2TBfZ7","parent_uuid":null,"doc_id":null,"level":0,"id":null,"open_window":1,"visible":1},{"type":"DOC","title":"读书笔记","uuid":"6905122:JHVTnwu3BB2TBfZ7","url":"chrh36","prev_uuid":"bna1nP6Jujruc0b_","sibling_uuid":"6905122:RJqDVhg_c_SlqBHP","child_uuid":null,"parent_uuid":"bna1nP6Jujruc0b_","doc_id":23953349,"level":1,"id":23953349,"open_window":1,"visible":1},{"type":"DOC","title":"学习计划","uuid":"6905122:RJqDVhg_c_SlqBHP","url":"wrbzgy","prev_uuid":"6905122:JHVTnwu3BB2TBfZ7","sibling_uuid":null,"child_uuid":null,"parent_uuid":"bna1nP6Jujruc0b_","doc_id":23953350,"level":1,"id":23953350,"open_window":1,"visible":1},{"type":"DOC","title":"技巧","uuid":"wfNAXnRxNzFjGbzP","url":"bqgx1h","prev_uuid":"bna1nP6Jujruc0b_","sibling_uuid":null,"child_uuid":"R3qrgfW7xGnSKpJv","parent_uuid":null,"doc_id":64875318,"level":0,"id":64875318,"open_window":0,"visible":1},{"type":"DOC","title":"MarkDown用法","uuid":"R3qrgfW7xGnSKpJv","url":"kk2wwz","prev_uuid":"wfNAXnRxNzFjGbzP","sibling_uuid":"OA5OgasGIzUAZjpS","child_uuid":null,"parent_uuid":"wfNAXnRxNzFjGbzP","doc_id":52300940,"level":1,"id":52300940,"open_window":1,"visible":1},{"type":"DOC","title":"Typora使用方法","uuid":"OA5OgasGIzUAZjpS","url":"lorlhvk7zq6z","prev_uuid":"R3qrgfW7xGnSKpJv","sibling_uuid":"4y4f8UHeLbU8uyDQ","child_uuid":null,"parent_uuid":"wfNAXnRxNzFjGbzP","doc_id":52301594,"level":1,"id":52301594,"open_window":1,"visible":1},{"type":"DOC","title":"MarkDown 常用HTML标记","uuid":"4y4f8UHeLbU8uyDQ","url":"ozru6yg52sts","prev_uuid":"OA5OgasGIzUAZjpS","sibling_uuid":"fmwOXK38xBC3gQiT","child_uuid":null,"parent_uuid":"wfNAXnRxNzFjGbzP","doc_id":52301586,"level":1,"id":52301586,"open_window":1,"visible":1},{"type":"DOC","title":"Chrome等浏览器技巧","uuid":"fmwOXK38xBC3gQiT","url":"ike4u1","prev_uuid":"4y4f8UHeLbU8uyDQ","sibling_uuid":null,"child_uuid":null,"parent_uuid":"wfNAXnRxNzFjGbzP","doc_id":64875374,"level":1,"id":64875374,"open_window":0,"visible":1}]'
    logger.info("%s", catalog_node_list_json)
    catalog_node_list = json.loads(catalog_node_list_json)
    logger.info("v1:%s", json.dumps(yuque_service.create_catalog_tree(catalog_node_list)))
    catalog_node_list = json.loads(catalog_node_list_json)
    logger.info("v2:%s", json.dumps(yuque_service.create_catalog_tree_v2(catalog_node_list, 'root')))
    catalog_node_list = json.loads(catalog_node_list_json)
    logger.info("v3:%s", json.dumps(yuque_service.create_catalog_tree_v3(catalog_node_list, 'root')))
    catalog_node_list = json.loads(catalog_node_list_json)
    logger.info("v4:%s", json.dumps(yuque_service.create_catalog_tree_v4(catalog_node_list, 'root', ".")))
    catalog_node_list = json.loads(catalog_node_list_json)
    yuque_service.add_path_to_catalog_node_list(catalog_node_list, 'root', ".")
    logger.info("path:%s", json.dumps(catalog_node_list))


def run_datetime():
    print("xxxxxxx")
    print(datetime.datetime.now().date())


run_datetime()
