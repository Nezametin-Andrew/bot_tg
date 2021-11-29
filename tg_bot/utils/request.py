import json
import urllib3


def get_url():
    return "http://localhost:8000/api/v1/"


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

    return json.loads(r.data.decode())