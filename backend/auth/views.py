import logging
import traceback

from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse
from rest_framework.request import Request
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework.views import APIView

from ..utils import Response
from .models import Session, User
from .serializers import UserSerializer

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    # noinspection PyMethodMayBeStatic
    def post(self, request: Request) -> HttpResponse:
        """
        This route is responsible for registering user.
        Args:
            request: HTTP request object
        Returns:
            Success 200 status code and a success message if user register
            successfully, return 400 status code otherwise.
        """
        try:
            email = request.data.get("email")
            password = request.data.get("password")
            first_name = request.data.get("first_name")
            last_name = request.data.get("last_name")
            phone_number = request.data.get("phone_number")
            if not (
                email
                and password
                and first_name
                and last_name
                and phone_number
            ):
                message = "Invalid Payload. Missing required  fields"
                return Response(
                    message=message,
                    status=HTTP_400_BAD_REQUEST,
                ).get_in_json()
            if User.objects.filter(email=email).exists():
                return Response(
                    message="Email ID already exists.",
                    status=HTTP_400_BAD_REQUEST,
                ).get_in_json()
            password = make_password(password)
            user_obj = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                password=password,
            )
            if user_obj:
                data = UserSerializer(instance=user_obj).data
                return Response(
                    data=data,
                    message="User registered Successfully",
                    status=HTTP_200_OK,
                ).get_in_json()
        except Exception as ex:
            logger.exception(ex)
            return Response(
                message="Something went wrong",
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            ).get_in_json()


class LoginView(APIView):
    # noinspection PyMethodMayBeStatic
    def post(self, request: Request) -> HttpResponse:
        """
        This route handles the login functionality of user.
        Args:
            request: HTTP request object
        Returns:
            User details along with session token if user login successfully.
        """
        try:
            email = request.data.get("email", "")
            password = request.data.get("password", "")
            user_obj = User.objects.filter(email=email).first()
            if not user_obj:
                return Response(
                    message="Email-ID does not exist",
                    status=HTTP_400_BAD_REQUEST,
                ).get_in_json()
            if check_password(password, user_obj.password):
                result = UserSerializer(instance=user_obj).data
                result["session_id"] = Session.generate_token(user_obj)
                return Response(
                    data=result,
                    message="User Signed In Successfully",
                    status=HTTP_200_OK,
                ).get_in_json()
            else:
                return Response(
                    message="Invalid Credentials",
                    status=HTTP_400_BAD_REQUEST,
                ).get_in_json()
        except Exception as ex:
            logger.exception(ex)
            return Response(
                message="Something went wrong",
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            ).get_in_json()


class LogoutView(APIView):
    # noinspection PyMethodMayBeStatic
    def post(self, request: Request) -> HttpResponse:
        """
        This route is responsible for clearing out the user session.
        Args:
            request: HTTP request object
        Returns:
            Success message if user logout successfully.
        """
        try:
            session_id = request.META.get("HTTP_X_SESSION_ID")
            session_obj = Session.objects.filter(session_id=session_id).update(
                is_active=False
            )
            if session_obj:
                return Response(
                    message="User Logged Out Successfully", status=HTTP_200_OK
                ).get_in_json()
            return Response(
                message="Error occurred while logging out user.",
                status=HTTP_400_BAD_REQUEST,
            ).get_in_json()
        except Exception as ex:
            logger.exception(ex)
            return Response(
                message="Something went wrong",
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            ).get_in_json()
