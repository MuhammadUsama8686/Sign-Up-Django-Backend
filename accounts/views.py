# accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer


class SignupAPIView(APIView):
    """
    POST /accounts/signup/
    Always returns: { "message": "Single error or success message" }
    Only ONE error at a time (clean & user-friendly)
    """

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)

        if not serializer.is_valid():
            # Get ONLY the first error (from the first field)
            first_field = next(iter(serializer.errors))  # e.g., 'full_name', 'email', 'password'
            first_error = serializer.errors[first_field][0]  # First message only
            message = str(first_error)

            # 409 only for duplicate email
            if first_field == "email" and "exists" in message.lower():
                return Response({"message": message}, status=status.HTTP_409_CONFLICT)

            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

        # Success
        serializer.save()
        return Response(
            {"message": "Account created successfully!"},
            status=status.HTTP_201_CREATED
        )