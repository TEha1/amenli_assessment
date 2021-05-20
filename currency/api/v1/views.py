from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utilities.exceptions import Http400
from utilities.helpers import get_converted_currency_amount
from currency.api.v1.serializers import (
    CurrencySerializer, CurrencyDetailSerializer, UserLoginSerializer,
    UserLoginDataSerializer
)


class CurrencyConverterAPIView(CreateAPIView):
    serializer_class = CurrencySerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            money = get_converted_currency_amount(
                amount=data['amount'],
                from_currency=data['from_currency_type'],
                to_currency=data['to_currency_type'],
            )
            data['converted_amount'] = money
            data['user'] = self.request.user
        except ValueError as error:
            raise Http400(str(error))

        self.perform_create(serializer)
        return Response(CurrencyDetailSerializer(data).data, status=status.HTTP_200_OK)


class UserLoginAPIView(GenericAPIView):
    serializer_class = UserLoginSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = authenticate(
            username=data['username'],
            password=data['password'],
        )
        if user:
            return Response(
                data=UserLoginDataSerializer(user).data
            )
        raise AuthenticationFailed()
