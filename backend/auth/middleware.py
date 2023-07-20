from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from ..utils import Response
from .models import Session
from .views import LoginView, RegisterView


class SessionCheckMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    # noinspection PyMethodMayBeStatic
    def process_view(self, request, view, *args, **kwargs):
        if request.path != "/" and view.view_class not in (
            LoginView,
            RegisterView,
        ):
            session_id = request.META.get("HTTP_X_SESSION_ID")
            if not session_id:
                return Response(
                    message="Invalid Request",
                    status=HTTP_400_BAD_REQUEST,
                ).get_in_json()
            session_obj = Session.objects.filter(
                session_id=session_id, is_active=True
            ).first()
            if session_obj:
                request.user_obj = session_obj.user
            else:
                return Response(
                    message="Unauthorized User",
                    status=HTTP_401_UNAUTHORIZED,
                ).get_in_json()
