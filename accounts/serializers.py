# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Profile
from django.core.exceptions import ValidationError as DjangoValidationError


class SignupSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    phone = serializers.CharField(max_length=50, allow_blank=True, required=False)
    country = serializers.CharField(max_length=100, allow_blank=True, required=False)
    city = serializers.CharField(max_length=100, allow_blank=True, required=False)
    address = serializers.CharField(max_length=500, allow_blank=True, required=False)
    zip_code = serializers.CharField(max_length=20, allow_blank=True, required=False)

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            # Return ONLY the FIRST password error
            if e.messages:
                raise serializers.ValidationError(e.messages[0])
            raise serializers.ValidationError("Invalid password.")
        return value

    def create(self, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        full_name = validated_data.pop("full_name", "")

        user = User.objects.create_user(username=email, email=email, password=password)

        Profile.objects.create(
            user=user,
            full_name=full_name,
            phone=validated_data.get("phone", ""),
            country=validated_data.get("country", ""),
            city=validated_data.get("city", ""),
            address=validated_data.get("address", ""),
            zip_code=validated_data.get("zip_code", ""),
        )
        return user