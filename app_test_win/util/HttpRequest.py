import pprint
import re
import requests
import base64


class HttpRequest(object):

    @staticmethod
    def request_api(path, token, server_url, method="GET", **kwargs):
        """
        get info from ATXserver2
        :return:
        """
        kwargs['headers'] = {"Authorization": "Bearer " + token}
        server_url += path
        try:
            if not re.match(r'^http?:/{2}\w.+$', server_url):
                raise Exception('url error', server_url)
            r = requests.request(method, server_url, **kwargs)
            r.raise_for_status()
        except requests.HTTPError:
            raise
        return r.json()


if __name__ == '__main__':
    a = HttpRequest
    print(a.request_api("/api/v1/devices", 'dad7ed9920dd4a1f96b5e8ddd1a6d4bd', 'http://10.15.10.209:8998',
          params={"usable": "true"}))
