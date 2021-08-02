from typing import Any

from requests import Response, Session


class Client:
    def __init__(self, host: str, **kwargs: Any) -> None:
        self.host = host
        self.kwargs = kwargs
        self.session = Session()

    def request(self, method: str, path: str, **kwargs: Any) -> Response:
        if path.startswith('/'):
            path = path[1:]
        request_kwargs = dict(**self.kwargs)
        request_kwargs.update(**kwargs)
        request_kwargs["method"] = method
        request_kwargs["url"] = f"{self.host}/{path}"
        response = self.session.request(**request_kwargs)
        response.raise_for_status()
        return response
