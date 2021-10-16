from rest_framework.response import Response
from rest_framework import exceptions
from user_app.models import Account as User
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, SignUpSerializer
from django.contrib.auth import logout
from rest_framework_jwt.settings import api_settings
from django.shortcuts import get_object_or_404


@permission_classes((permissions.AllowAny,))
class UserApis(viewsets.ViewSet):  # User class
    """this class includes all the basic operations related to user"""

    @action(detail=False, methods=['post'])
    def sign_up(self, request):
        serializer = SignUpSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "User Registered."
            data['email'] = account.email
            data['username'] = account.username
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        email = request.data.get('email')
        password = request.data.get('password')
        if (email is None) or (password is None):
            raise exceptions.AuthenticationFailed(
                'email and password required')
        user = User.objects.filter(email=email).first()
        if(user is None):
            raise exceptions.AuthenticationFailed('user not found')
        if (not user.check_password(password)):
            raise exceptions.AuthenticationFailed('wrong password')
        serialized_user = UserSerializer(user).data
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        data = {
            'access_token': token,
            'payload': payload,
            'user_info': serialized_user,
        }
        return Response(data, status=status.HTTP_200_OK)
    
    # authentication requried views

    @action(detail=False, methods=['put', 'get'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        user_obj = get_object_or_404(User, id=request.user.id)
        serializer = UserSerializer(user_obj)
        if request.method == "PUT":
            serializer = UserSerializer(user_obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                data = serializer.errors
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def sign_out(self, request):
        logout(request)
        return Response({"msg":"Logged out"}, status=status.HTTP_200_OK)
