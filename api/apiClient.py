import requests


class APIClient:

    def __init__(self, base_url, timeout=10, headers=None):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

        if headers:
            self.session.headers.update(headers)

    def set_token(self, token):
        self.session.headers.update({
            "Authorization": f"Bearer {token}"
        })


    def get(self, endpoint, **kwargs):
        return self.session.get(
            self._build_url(endpoint), timeout=self.timeout, **kwargs
            )

    def post(self, endpoint, json=None, **kwargs):
        return self.session.post(
            self._build_url(endpoint), json=json, timeout=self.timeout, **kwargs
        )

    def put(self, endpoint, json=None, **kwargs):
        return self.session.put(
            self._build_url(endpoint), json=json, timeout=self.timeout, **kwargs
        )

    def delete(self, endpoint, **kwargs):
        return self.session.delete(
            self._build_url(endpoint), timeout=self.timeout, **kwargs
        )

    def _build_url(self, endpoint):
        return f"{self.base_url}/{endpoint.lstrip('/')}"