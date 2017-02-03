import requests

from unsplash.error import UnsplashError


class Client(object):

    def __init__(self, api, **kwargs):
        self.api = api

    def _request(self, url, method, params=None, data=None, **kwargs):
        url = "%s%s" % (self.api.base_url, url)
        headers = self.get_auth_header()
        headers.update(kwargs.get("headers", {}))
        response = requests.request(method, url, params=params, data=data, headers=headers, **kwargs)

        if not self._is_2xx(response.status_code):
            errors = response.json().get("errors")
            raise UnsplashError(errors[0] if errors else None)
        return response

    def _get(self, url, params=None, **kwargs):
        return self._request(url, "get", params=params, **kwargs)

    def _post(self, url, data=None, **kwargs):
        return self._request(url, "post", data=data, **kwargs)

    def _delete(self, url, **kwargs):
        return self._request(url, "delete", **kwargs)

    def _put(self, url, data=None, **kwargs):
        return self._request(url, "put", data=data, **kwargs)

    def get_auth_header(self):
        return {"Authorization": "Bearer %s" % self.api.access_token}

    @staticmethod
    def _is_1xx(status_code):
        return 100 <= status_code <= 199

    @staticmethod
    def _is_2xx(status_code):
        return 200 <= status_code <= 299

    @staticmethod
    def _is_3xx(status_code):
        return 300 <= status_code <= 399

    @staticmethod
    def _is_4xx(status_code):
        return 400 <= status_code <= 499

    @staticmethod
    def _is_5xx(status_code):
        return 500 <= status_code <= 599
