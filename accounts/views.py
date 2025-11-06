from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer

class SignupAPIView(APIView):
    """
    POST /api/signup/ 
    Accepts JSON with the fields shown in the form (full_name, email, password, phone, country, city, address, zip_code)
    """

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            # if email already exists we want to send 409
            errors = serializer.errors
            if "email" in errors and any("exists" in str(m).lower() for m in errors["email"]):
                return Response(errors, status=status.HTTP_409_CONFLICT)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        profile = user.profile
        data = {
            "id": user.id,
            "email": user.email,
            "full_name": profile.full_name,
            "phone": profile.phone,
            "country": profile.country,
            "city": profile.city,
            "address": profile.address,
            "zip_code": profile.zip_code,
        }
        return Response(data, status=status.HTTP_201_CREATED)
