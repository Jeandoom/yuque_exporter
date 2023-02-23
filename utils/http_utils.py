import json

import requests


def get(url, params=None, headers={}):
    response = requests.get(url, params=params, headers=headers)
    if isJsonFormat(headers):
        return json.loads(response.content)
    return response.content


def download(url, params=None, headers={}):
    # return requests.get(url, params=params, headers=headers)
    response = requests.get(url, params=params, headers=headers)
    return response.content


def post(url, data=None, headers={}):
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if isJsonFormat(headers):
        return json.loads(response.content)
    return response.content


def put(url, data=None, headers={}):
    response = requests.put(url, data=json.dumps(data), headers=headers)
    if isJsonFormat(headers):
        return json.loads(response.content)
    return response.content


def isJsonFormat(headers={}):
    if headers.get("Content-Type") is None:
        return False
    return headers.get("Content-Type").find("application/json") > -1


