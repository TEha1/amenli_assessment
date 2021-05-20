from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from currency.models import UserCurrency

User = get_user_model()


class CurrencySerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(
        decimal_places=2,
        max_digits=12,
        required=True
    )
    converted_amount = serializers.DecimalField(
        decimal_places=2,
        max_digits=12,
        read_only=True,
    )

    class Meta:
        model = UserCurrency
        fields = [
            'id',
            'user',
            'amount',
            'from_currency_type',
            'to_currency_type',
            'converted_amount',
            'times',
        ]
        extra_kwargs = {
            'user': {'read_only': True, },
        }

    def create(self, validated_data):
        validated_data.pop('amount', None)
        validated_data.pop('converted_amount', None)
        user_currency = UserCurrency.objects.filter(
            user=validated_data['user'],
            from_currency_type=validated_data['from_currency_type'],
            to_currency_type=validated_data['to_currency_type']
        ).first()
        if user_currency:
            user_currency.times += 1
            user_currency.save()
            return user_currency
        return super(CurrencySerializer, self).create(validated_data)


class CurrencyDetailSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(
        decimal_places=2,
        max_digits=12,
        read_only=True
    )
    converted_amount = serializers.DecimalField(
        decimal_places=2,
        max_digits=12,
        read_only=True,
    )

    class Meta:
        model = UserCurrency
        fields = [
            'amount',
            'from_currency_type',
            'to_currency_type',
            'converted_amount',
            'times',
        ]


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserLoginDataSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField('get_token')

    class Meta:
        model = User
        fields = [
            'token',
            'id',
            'email',
            'username',
        ]

    def get_token(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return token.key
