# utf-8
import json
import os
import stringutils

from utils import log_utils
from utils import http_utils
from dotenv import load_dotenv

global COOKIE

load_dotenv()
COOKIE = os.environ["yuque_cookie"]
logger = log_utils.get_logger('yuque_service')

COOKIE = "lang=zh-cn; _yuque_session=Wp4jcnzLxQz_Ipaz8d5WOIbDK6rjWrW3UaubRIV7wlDEe1r9GNYNaHBUNpuO4hgu4wA1PUsJCSCncmwTojdXsw==; yuque_ctoken=jKGqoi-6Ikel-ouyXdSkvc5d; acw_tc=0bca293616755015492492845ecd49ad61620af558b22f48b3c9d7f19c19b3"
hostUrl = "https://www.yuque.com"

headers = {"Accept": "application/json",
           "Content-Type": "application/json",
           "cookie": COOKIE,
           # x-csrf-token取cookie中的yuque_ctoken的值
           "x-csrf-token": "jKGqoi-6Ikel-ouyXdSkvc5d"
           }
download_headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "if-none-match": "149-YahvrX+LB+i3tQ73UG3s5vZ7FQI",
    "sec-ch-ua": '"Not_A Brand";v="99", "Microsoft Edge";v="109", "Chromium";v="109"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "cookie": COOKIE,
    # x-csrf-token取cookie中的yuque_ctoken的值
    "x-csrf-token": "jKGqoi-6Ikel-ouyXdSkvc5d"
    }


def get_catalog_by_lib_id(lib_id):
    path = "/api/docs"
    params = {"book_id": lib_id}
    requestUrl = hostUrl + path
    # requestUrl = hostUrl + path+"?"+param+"="+lib_id
    return http_utils.get(requestUrl, params=params, headers=headers)


def get_blog_id_dict(catalog_resp={}):
    catalog = catalog_resp.get("data")
    blog_id_dict = {}
    for index in catalog:
        blog_id_dict[index.get("id")] = index
    return blog_id_dict


def getMarkDownFileExport(blog_id_dict: {}):
    markdown_file_export_dict = {}
    for blog_id, blog_index in blog_id_dict.items():
        markdown_file_export = "https://www.yuque.com/api/docs/" + str(blog_id) + "/export"
        markdown_file_export_dict[blog_id] = markdown_file_export
    return markdown_file_export_dict


def getMarkDownFileDownload(markdown_file_export_dict: {}):
    markdown_file_download_dict = {}
    req_data = {"type": "markdown", "force": 0, "options": "{\"latexType\":1}"}
    for blog_id, url in markdown_file_export_dict.items():
        try:
            response = http_utils.post(url, data=req_data, headers=headers)
            logger.debug("markdown_file_export resp data:%s", response)
            resp_data = response.get("data")
            if resp_data is None:
                markdown_file_download_dict[blog_id] = response
                continue
            if "success" == resp_data.get("state"):
                markdown_file_download_dict[blog_id] = resp_data.get("url")
        except Exception as e:
            logger.error("%s", e)
    return markdown_file_download_dict


def publish_blog(blog_id_list: []):
    for blog_id in blog_id_list:
        markdown_file_export = "https://www.yuque.com/api/docs/" + str(blog_id) + "/publish"
        req_data = {"force": False, "notify": False, "cover": None, "ignoreGlobalMessage": True}
        response = http_utils.put(markdown_file_export, data=req_data, headers=headers)
        logger.debug("publish_blog resp data:%s", response)


def get_export_error_retry_id_list(markdown_file_download_dict: {}):
    export_error_retry_id_list = []
    for blog_id, export_resp in markdown_file_download_dict.items():
        if isinstance(export_resp, dict):
            if export_resp.get("status") == 400:
                if export_resp.get("message") == "请发布后再导出":
                    export_error_retry_id_list.append(blog_id)
    return export_error_retry_id_list


def get_retry_dict(markdown_file_export_dict, export_error_retry_id_list):
    markdown_file_export_retry_dict = {}
    for blog_id in export_error_retry_id_list:
        markdown_file_export_retry_dict[blog_id] = markdown_file_export_dict[blog_id]
    return markdown_file_export_retry_dict


def download_markdown_file_download_dict(download_markdown_file_download_dict: {}, blog_id_dict: {},
                                         directory_name: 'default'):
    for blog_id, download_url in download_markdown_file_download_dict.items():
        index = blog_id_dict[blog_id]
        mkDir(directory_name)
        download(download_url, file_name_format(index.get("title")), directory_name)


def download_markdown_file_download_dict_v2(download_markdown_file_download_dict: {}, catalog_node_dict):
    for blog_id, download_url in download_markdown_file_download_dict.items():
        try:
            catalog_node = catalog_node_dict[blog_id]

            parent_path = catalog_node.get("parent_path")
            title = catalog_node.get("title")

            if str_is_not_blank(catalog_node.get("child_uuid")):
                parent_path = parent_path + "/" + title

            mkDir(parent_path)
            download(download_url, file_name_format(catalog_node.get("title")), parent_path)
        except Exception as e:
            logger.error("download_error:blog_id[%s],download_url[%s]", blog_id, download_url)


def file_name_format(file_name: ''):
    return file_name \
        .replace("\r", "") \
        .replace("/", "or") \
        .replace("(", "（") \
        .replace(")", "）") \
        .replace(">", "》") \
        .replace("<", "《") \
        .replace("\"", "'") \
        .replace(":", "：") \
        .replace("*", "+") \
        .replace("?", "？")


def mkDir(dir):
    is_exists = os.path.exists(dir)
    if not is_exists:
        os.makedirs(dir)


def download(download_url, file_name: '', directory_name: 'default'):
    data = http_utils.download(download_url, None, download_headers)
    logger.info("%s", data)
    # logger.info("%s", data.content)
    with open(directory_name + "/" + file_name + '.md', 'wb') as f:
        f.write(data)


def download_lib_dict(lib_dict: {}):
    for lib_id, lib in lib_dict.items():
        try:
            download_lib(lib)
        except Exception as e:
            logger.error("error_lib_info:%s", json.dumps(lib))
            logger.error("%s", e)



def download_lib(lib: {}):
    # logger.info("%s",headers.get("Content-Type").find("application/json")>-1)
    logger.info("get_catalog_by_libId")
    catalog_node_list = get_catalog_node_list(lib["target_id"])
    add_path_to_catalog_node_list(catalog_node_list, 'root', "./exported/"+lib["target"]["name"])
    catalog_node_dict = convert_list_to_dict(catalog_node_list, 'doc_id')
    logger.info("catalog_node_dict:%s", json.dumps(catalog_node_dict))
    lib_catalog = get_catalog_by_lib_id(str(lib["target_id"]))
    logger.info("lib_catalog:%s", json.dumps(lib_catalog))
    blog_id_dict = get_blog_id_dict(lib_catalog)
    logger.info("blog_id_dict:%s", json.dumps(blog_id_dict))
    markdown_file_export_dict = getMarkDownFileExport(blog_id_dict)
    # markdown_file_export_dict = getMarkDownFileExportUrl([52301594])
    logger.info("markdown_file_export_dict:%s", json.dumps(markdown_file_export_dict))
    markdown_file_download_dict = getMarkDownFileDownload(markdown_file_export_dict)
    logger.info("markdown_file_download_dict:%s", json.dumps(markdown_file_download_dict))
    export_error_retry_id_list = get_export_error_retry_id_list(markdown_file_download_dict)
    logger.info("export_error_retry_id_list:%s", json.dumps(export_error_retry_id_list))
    if export_error_retry_id_list.__len__() > 0:
        publish_blog(export_error_retry_id_list)
        logger.info("publish_blog: done")
        markdown_file_export_dict = get_retry_dict(markdown_file_export_dict, export_error_retry_id_list)
        logger.info("markdown_file_export_dict:%s", json.dumps(markdown_file_export_dict))
        markdown_file_download_dict.update(getMarkDownFileDownload(markdown_file_export_dict))
        logger.info("markdown_file_export_retry_dict:%s", json.dumps(markdown_file_download_dict))
    download_markdown_file_download_dict_v2(markdown_file_download_dict, catalog_node_dict)


def convert_list_to_dict(req_list: [], key: ''):
    resp_dict = {}
    for item in req_list:
        resp_dict[item.get(key)] = item
    return resp_dict


# response catalog_node_list.json
# GET
# param = {"book_id": 6905122, "format": "list", "node_uuid": "qIGFgI5-T-qA2joE", "action": "edit", "title": "kkkk"}
def get_catalog_node_list(lib_id: ''):
    url = "https://www.yuque.com/api/catalog_nodes"
    param = {"book_id": lib_id}
    response = http_utils.get(url, param, headers=headers)
    logger.debug("get_catalog_node_list resp data:%s", json.dumps(response))
    resp_data = response.get("data")
    if resp_data is not None:
        return resp_data


def get_lib_dict():
    url = "https://www.yuque.com/api/mine/common_used?"
    resp_data = http_utils.get(url, None, headers)
    # 查询返回示例
    # {"meta":{"changed":true},"data":{"groups":[],"books":[{"id":4861874441,"user_id":8432833,"organization_id":0,"type":"Book","icon":null,"title":"默认知识库","url":"/go/book/6905092","order_num":0,"target_id":6905092,"target_type":"Book","created_at":"2022-04-07T14:08:45.000Z","updated_at":"2022-04-09T05:47:47.000Z","ref_id":"dashboard_books","target":{"id":6905092,"type":"Book","slug":"kb","name":"默认知识库","user_id":8432833,"description":null,"creator_id":8432833,"public":0,"scene":null,"created_at":"2020-12-22T12:27:47.000Z","updated_at":"2023-02-06T11:32:26.000Z","content_updated_at":"2022-05-11T01:10:06.509Z","archived_at":null,"organization_id":0,"enable_auto_publish":true,"privacy_migrated":true,"user":null,"_serializer":"web.book_lite"},"user":{"id":8432833,"type":"User","login":"rainco","name":"Rainco","avatar":"https://cdn.nlark.com/yuque/0/2021/png/8432833/1632801197519-avatar/a24027c5-29fd-4951-afa2-be5ab015a178.png","scene":null,"avatar_url":"https://cdn.nlark.com/yuque/0/2021/png/8432833/1632801197519-avatar/a24027c5-29fd-4951-afa2-be5ab015a178.png","role":1,"isPaid":false,"member_level":1,"followers_count":0,"following_count":2,"description":"🚜☁️☁️","status":1,"_serializer":"web.user_lite"},"_serializer":"web.quick_link"},{"id":4861874444,"user_id":8432833,"organization_id":0,"type":"Book","icon":null,"title":"学习笔记","url":"/go/book/6905122","order_num":1,"target_id":6905122,"target_type":"Book","created_at":"2022-04-07T14:08:45.000Z","updated_at":"2022-04-09T05:47:47.000Z","ref_id":"dashboard_books","target":{"id":6905122,"type":"Book","slug":"zzhta4","name":"学习笔记","user_id":8432833,"description":"点滴学习，随时记录","creator_id":8432833,"public":0,"scene":"notes","created_at":"2020-12-22T12:35:01.000Z","updated_at":"2023-02-06T14:04:01.000Z","content_updated_at":"2023-02-06T14:04:00.814Z","archived_at":null,"organization_id":0,"enable_auto_publish":false,"privacy_migrated":true,"user":null,"_serializer":"web.book_lite"},"user":{"id":8432833,"type":"User","login":"rainco","name":"Rainco","avatar":"https://cdn.nlark.com/yuque/0/2021/png/8432833/1632801197519-avatar/a24027c5-29fd-4951-afa2-be5ab015a178.png","scene":null,"avatar_url":"https://cdn.nlark.com/yuque/0/2021/png/8432833/1632801197519-avatar/a24027c5-29fd-4951-afa2-be5ab015a178.png","role":1,"isPaid":false,"member_level":1,"followers_count":0,"following_count":2,"description":"🚜☁️☁️","status":1,"_serializer":"web.user_lite"},"_serializer":"web.quick_link"},{"id":4861874446,"user_id":8432833,"organization_id":0,"type":"Book","icon":null,"title":"Maycur","url":"/go/book/20978116","order_num":2,"target_id":20978116,"target_type":"Book","created_at":"2022-04-07T14:08:45.000Z","updated_at":"2022-04-09T05:47:47.000Z","ref_id":"dashboard_books","target":{"id":20978116,"type":"Book","slug":"fpbksm","name":"Maycur","user_id":8432833,"description":"","creator_id":8432833,"public":0,"scene":null,"created_at":"2021-09-28T03:01:13.000Z","updated_at":"2023-02-07T07:15:50.000Z","content_updated_at":"2023-02-06T01:55:00.659Z","archived_at":null,"organization_id":0,"enable_auto_publish":true,"privacy_migrated":true,"user":null,"_serializer":"web.book_lite"},"user":{"id":8432833,"type":"User","login":"rainco","name":"Rainco","avatar":"https://cdn.nlark.com/yuque/0/2021/png/8432833/1632801197519-avatar/a24027c5-29fd-4951-afa2-be5ab015a178.png","scene":null,"avatar_url":"https://cdn.nlark.com/yuque/0/2021/png/8432833/1632801197519-avatar/a24027c5-29fd-4951-afa2-be5ab015a178.png","role":1,"isPaid":false,"member_level":1,"followers_count":0,"following_count":2,"description":"🚜☁️☁️","status":1,"_serializer":"web.user_lite"},"_serializer":"web.quick_link"},{"id":4861874448,"user_id":8432833,"organization_id":0,"type":"Book","icon":null,"title":"技术栈","url":"/go/book/20684276","order_num":4,"target_id":20684276,"target_type":"Book","created_at":"2022-04-07T14:08:45.000Z","updated_at":"2022-04-09T05:47:47.000Z","ref_id":"dashboard_books","target":{"id":20684276,"type":"Book","slug":"bdreeb","name":"Tech Stack","user_id":8432833,"description":"","creator_id":8432833,"public":0,"scene":null,"created_at":"2021-08-31T03:51:12.000Z","updated_at":"2023-01-21T04:17:47.000Z","content_updated_at":"2023-01-21T04:17:47.112Z","archived_at":null,"organization_id":0,"enable_auto_publish":true,"privacy_migrated":true,"user":null,"_serializer":"web.book_lite"},"user":{"id":8432833,"type":"User","login":"rainco","name":"Rainco","avatar":"https://cdn.nlark.com/yuque/0/2021/png/8432833/1632801197519-avatar/a24027c5-29fd-4951-afa2-be5ab015a178.png","scene":null,"avatar_url":"https://cdn.nlark.com/yuque/0/2021/png/8432833/1632801197519-avatar/a24027c5-29fd-4951-afa2-be5ab015a178.png","role":1,"isPaid":false,"member_level":1,"followers_count":0,"following_count":2,"description":"🚜☁️☁️","status":1,"_serializer":"web.user_lite"},"_serializer":"web.quick_link"},{"id":4861874449,"user_id":8432833,"organization_id":0,"type":"Book","icon":null,"title":"Self Media","url":"/go/book/24750617","order_num":5,"target_id":24750617,"target_type":"Book","created_at":"2022-04-07T14:08:45.000Z","updated_at":"2022-04-09T05:47:47.000Z","ref_id":"dashboard_books","target":{"id":24750617,"type":"Book","slug":"abix3e","name":"Self Media","user_id":8432833,"description":"","creator_id":8432833,"public":0,"scene":null,"created_at":"2022-02-13T04:48:43.000Z","updated_at":"2022-06-08T17:17:55.000Z","content_updated_at":"2022-02-13T05:55:35.868Z","archived_at":null,"organization_id":0,"enable_auto_publish":true,"privacy_migrated":true,"user":null,"_serializer":"web.book_lite"},"user":{"id":8432833,"type":"User","login":"rainco","name":"Rainco","avatar":"https://cdn.nlark.com/yuque/0/2021/png/8432833/1632801197519-avatar/a24027c5-29fd-4951-afa2-be5ab015a178.png","scene":null,"avatar_url":"https://cdn.nlark.com/yuque/0/2021/png/8432833/1632801197519-avatar/a24027c5-29fd-4951-afa2-be5ab015a178.png","role":1,"isPaid":false,"member_level":1,"followers_count":0,"following_count":2,"description":"🚜☁️☁️","status":1,"_serializer":"web.user_lite"},"_serializer":"web.quick_link"},{"id":5940143903,"user_id":8432833,"organization_id":0,"type":"Book","icon":null,"title":"Diary","url":"/go/book/27780490","order_num":12,"target_id":27780490,"target_type":"Book","created_at":"2022-11-17T16:00:04.000Z","updated_at":"2022-11-17T16:00:04.000Z","ref_id":"dashboard_books","target":{"id":27780490,"type":"Book","slug":"gosofe","name":"Diary","user_id":8432833,"description":"","creator_id":8432833,"public":0,"scene":null,"created_at":"2022-05-11T01:09:08.000Z","updated_at":"2022-06-08T20:11:20.000Z","content_updated_at":"2022-05-11T01:10:42.914Z","archived_at":null,"organization_id":0,"enable_auto_publish":true,"privacy_migrated":true,"user":null,"_serializer":"web.book_lite"},"user":{"id":8432833,"type":"User","login":"rainco","name":"Rainco","avatar":"https://cdn.nlark.com/yuque/0/2021/png/8432833/1632801197519-avatar/a24027c5-29fd-4951-afa2-be5ab015a178.png","scene":null,"avatar_url":"https://cdn.nlark.com/yuque/0/2021/png/8432833/1632801197519-avatar/a24027c5-29fd-4951-afa2-be5ab015a178.png","role":1,"isPaid":false,"member_level":1,"followers_count":0,"following_count":2,"description":"🚜☁️☁️","status":1,"_serializer":"web.user_lite"},"_serializer":"web.quick_link"},{"id":5940143904,"user_id":8432833,"organization_id":0,"type":"Book","icon":null,"title":"On Java 8","url":"/go/book/32207768","order_num":13,"target_id":32207768,"target_type":"Book","created_at":"2022-11-17T16:00:04.000Z","updated_at":"2022-11-17T16:00:04.000Z","ref_id":"dashboard_books","target":{"id":32207768,"type":"Book","slug":"ex0xli","name":"On Java 8","user_id":8432833,"description":"","creator_id":8432833,"public":0,"scene":null,"created_at":"2022-08-24T07:19:54.000Z","updated_at":"2022-08-24T07:27:56.000Z","content_updated_at":"2022-08-24T07:27:56.308Z","archived_at":null,"organization_id":0,"enable_auto_publish":true,"privacy_migrated":true,"user":null,"_serializer":"web.book_lite"},"user":{"id":8432833,"type":"User","login":"rainco","name":"Rainco","avatar":"https://cdn.nlark.com/yuque/0/2021/png/8432833/1632801197519-avatar/a24027c5-29fd-4951-afa2-be5ab015a178.png","scene":null,"avatar_url":"https://cdn.nlark.com/yuque/0/2021/png/8432833/1632801197519-avatar/a24027c5-29fd-4951-afa2-be5ab015a178.png","role":1,"isPaid":false,"member_level":1,"followers_count":0,"following_count":2,"description":"🚜☁️☁️","status":1,"_serializer":"web.user_lite"},"_serializer":"web.quick_link"}]}}
    lib_dict = {}
    if resp_data.get("data") is not None and resp_data.get("data").get("books") is not None:
        for lib in resp_data["data"]["books"]:
            lib_dict[lib["id"]] = lib
    return lib_dict

# 迭代算法实现，iteration
def create_catalog_tree(catalog_node_list: []):
    catalog_tree = {}
    for catalog_node in catalog_node_list:
        parent_uuid: str = catalog_node.get('parent_uuid')
        if parent_uuid is not None:
            if parent_uuid not in catalog_tree:
                catalog_tree[parent_uuid] = []
            catalog_tree[parent_uuid].append(catalog_node)

    return catalog_tree


# 迭代算法实现，iteration
def create_catalog_tree_v2(catalog_node_list: [], root_name: ''):
    catalog_tree = {}
    for catalog_node in catalog_node_list:
        parent_uuid: str = catalog_node.get('parent_uuid')
        if parent_uuid is None:
            parent_uuid = 'root'
        if parent_uuid not in catalog_tree:
            catalog_tree[parent_uuid] = []
        catalog_tree[parent_uuid].append(catalog_node)

    return catalog_tree


# 递归算法实现，recursion
def create_catalog_tree_v3(catalog_node_list: [], parent_name: ''):
    node_list = []
    for catalog_node in catalog_node_list:
        if catalog_node.get("fixed") is not None and catalog_node.get("fixed") is True:
            continue
        parent_uuid: str = catalog_node.get('parent_uuid')
        if (parent_uuid is None and parent_name == 'root') or parent_uuid == parent_name:
            parent_uuid = parent_name
            node_list.append(catalog_node)
            catalog_node["fixed"] = True
            child_uuid: str = catalog_node.get('child_uuid')
            if child_uuid is not None:
                child_node_list = create_catalog_tree_v3(catalog_node_list, catalog_node['uuid'])
                catalog_node['child_node_list'] = child_node_list
    return node_list


# 递归算法实现，recursion
# 添加path和parent_path属性
def create_catalog_tree_v4(catalog_node_list: [], parent_name: '', parent_path: ''):
    node_list = []
    for catalog_node in catalog_node_list:
        if catalog_node.get("fixed") is not None and catalog_node.get("fixed") is True:
            continue
        parent_uuid: str = catalog_node.get('parent_uuid')
        if (parent_uuid is None and parent_name == 'root') or parent_uuid == parent_name:
            parent_uuid = parent_name
            node_list.append(catalog_node)
            catalog_node["parent_path"] = parent_path
            catalog_node["path"] = parent_path + "/" + catalog_node["title"]
            catalog_node["fixed"] = True
            child_uuid: str = catalog_node.get('child_uuid')
            if child_uuid is not None:
                child_node_list = create_catalog_tree_v4(catalog_node_list, catalog_node['uuid'], catalog_node["path"])
                catalog_node['child_node_list'] = child_node_list
    return node_list


# 递归算法实现，recursion
# 添加path和parent_path属性,仅改变list值
def add_path_to_catalog_node_list(catalog_node_list: [], parent_name: '', parent_path: ''):
    for catalog_node in catalog_node_list:
        if catalog_node.get("fixed") is not None and catalog_node.get("fixed") is True:
            continue
        parent_uuid: str = catalog_node.get('parent_uuid')
        if ((str_is_blank(parent_uuid)) and parent_name == 'root') or parent_uuid == parent_name:
            catalog_node["parent_path"] = parent_path
            catalog_node["path"] = parent_path + "/" + catalog_node["title"]
            catalog_node["fixed"] = True
            child_uuid: str = catalog_node.get('child_uuid')
            if str_is_not_blank(child_uuid):
                add_path_to_catalog_node_list(catalog_node_list, catalog_node['uuid'], catalog_node["path"])


def get_directory_from_catalog_node_tree(catalog_node_tree):
    catalog_path_dict = {}
    for catalog_node in catalog_node_tree:
        if catalog_node.get("doc_id") is not None:
            catalog_path_dict[catalog_node['doc_id']] = catalog_node
    return catalog_path_dict



def str_is_blank(string: ''):
    return string is None or stringutils.is_whitespace(string)


def str_is_not_blank(string: ''):
    return not str_is_blank(string)


# main()
# download()
