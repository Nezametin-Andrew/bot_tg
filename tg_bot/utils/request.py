import json
import urllib3


def get_url():
    return "http://188.72.209.127/api/v1/"


def instance_http():
    return urllib3.PoolManager()


def request(model=None, method=None, data={}):
    url, http = get_url(), instance_http()
    data.update({'method': method})

    r = http.request(
        method="GET",
        url=url + model,
        fields=data

    )
    print(json.loads(r.data.decode()))
    return json.loads(r.data.decode())