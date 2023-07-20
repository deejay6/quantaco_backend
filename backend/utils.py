import json

from django.http import HttpResponse


class Response:
    def __init__(
        self, data: dict = None, message: str = "", status: int = 200
    ):
        if data is None:
            data = {}
        self.data = data
        self.status = status
        self.message = message

    def get_in_json(self) -> HttpResponse:
        content = {"data": self.data, "message": self.message}
        return HttpResponse(
            content=json.dumps(content),
            content_type="application/json",
            status=self.status,
        )
