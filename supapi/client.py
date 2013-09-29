# -*- coding:utf-8 -*-
import requests
from django.utils.http import urlencode


def _list_results(url, auth):
    results = []

    def get_results(url, results):
        req = requests.get(url, verify=False, auth=auth)
        if req.status_code == requests.codes.ok:
            data = req.json()
            if 'results' in data:
                results += data['results']
                next_url = data['next'] if 'next' in data else None
                if next_url:
                    get_results(next_url, results)
            else:
                results += data

    get_results(url, results)
    return results


def tuple_from_url(api_url, s, auth=None):
    results = []
    url = api_url
    if s:
        url = '{}{}/'.format(url, s)

    for item in _list_results(url, auth):
        if 'uid' in item and 'name' in item:
            results += (item['uid'], item['name']),
        else:
            results += (item[0], item[1]),
    return results


def list_from_url(api_url, params=None, auth=None, one_page=False, ):
    url = api_url
    if params:
        params = urlencode(params.items())
        url = '{}?{}'.format(api_url, params)
    if one_page:
        return _list_results(url, auth)
    req = requests.get(url, verify=False, auth=auth)
    if req.status_code == requests.codes.ok:
        return req.json()
    return []

