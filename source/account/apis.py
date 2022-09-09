from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserPasswordChangeSerializer, UsersSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from account.models import User


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistration(APIView):

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.save()
        #tokens = get_tokens_for_user(new_user)
        return Response({
            "status": status.HTTP_201_CREATED,
            #"tokens": tokens,
            "message": "User registration successful."
        })


class UserLogin(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        password = serializer.data.get("password")
        user = authenticate(username=email, password=password)
        if user:
            tokens = get_tokens_for_user(user)
            return Response({
                "status": status.HTTP_200_OK,
                "tokens": tokens,
                "message": "User login successful."
            })
        else:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "User login failed."
            })


class UserProfile(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request):
        print(request.user)
        serializer = UserProfileSerializer(request.user)
        
        return Response({
            "status": status.HTTP_200_OK,
            "user": serializer.data,
        })


class UserPasswordChange(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = UserPasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        new_password = serializer.data.get("password")
        print(serializer.data)
        user.set_password(new_password)
        user.save()
        return Response({
            "status": status.HTTP_200_OK,
            "message": "User password updated successfully."
        })


class UsersView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request):
        users = list(User.objects.all())
        serializer = UsersSerializer(data=users, many=True)
        serializer.is_valid(raise_exception=True)
        return Response({
            "status": status.HTTP_200_OK,
            "users": serializer.data
        })


