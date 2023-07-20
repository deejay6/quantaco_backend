import traceback

from django.http import HttpResponse
from rest_framework.request import Request
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework.views import APIView

from ..utils import Response
from .models import Customer
from .serializers import CustomerSerializer


class CustomerView(APIView):
    # noinspection PyMethodMayBeStatic
    def post(self, request: Request) -> HttpResponse:
        """
        This route is responsible for adding customer.
        Args:
            request: HTTP request object
        Returns:
            Success 200 status code and a success message if customer added
            successfully, return 400 status code otherwise.
        """
        try:
            name = request.data.get("customer_name")
            customer_id = request.data.get("customer_id")
            location = request.data.get("customer_location")
            if not all([name, customer_id, location]):
                message = "Invalid Payload. Missing required  fields"
                return Response(
                    message=message,
                    status=HTTP_400_BAD_REQUEST,
                ).get_in_json()
            if Customer.objects.filter(customer_id=customer_id).exists():
                return Response(
                    message="Customer already exists.",
                    status=HTTP_400_BAD_REQUEST,
                ).get_in_json()
            customer_obj = Customer.objects.create(
                name=name,
                customer_id=customer_id,
                location=location,
            )
            if customer_obj:
                data = CustomerSerializer(instance=customer_obj).data
                return Response(
                    data=data,
                    message="Customer added Successfully",
                    status=HTTP_200_OK,
                ).get_in_json()
        except Exception as ex:
            print(ex)
            traceback_string = traceback.format_exc()
            print(traceback_string)
            return Response(
                message="Something went wrong",
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            ).get_in_json()

    # noinspection PyMethodMayBeStatic
    def get(self, request: Request) -> HttpResponse:
        """
        This route is responsible for fetching customer list.
        Args:
            request: HTTP request object
        Returns:
            Success 200 status code and a success message if list
            fetched successfully.
        """
        try:
            result = []
            customer_obj_list = Customer.objects.all().order_by("-created_at")
            for customer_obj in customer_obj_list:
                customer = CustomerSerializer(instance=customer_obj).data
                result.append(customer)
            data = {"customers": result}
            return Response(
                data=data,
                message="Customer added Successfully",
                status=HTTP_200_OK,
            ).get_in_json()
        except Exception as ex:
            print(ex)
            traceback_string = traceback.format_exc()
            print(traceback_string)
            return Response(
                message="Something went wrong",
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            ).get_in_json()
