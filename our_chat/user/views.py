#from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView # for logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

# Use this class for Registration
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def get(self, request, *args, **kwargs):
        # Handle GET request logic here (e.g., render a registration form)
        return Response({"message": "Registration form"}, status=status.HTTP_200_OK)

    # Use the method to send the information of user
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# Use this class for login
class UserLoginView(ObtainAuthToken):
    error_messages = {
        'invalid': "Invalid username or password",
        'disabled': "Sorry, this account is suspended",
    }

    def _error_response(self, message_key):
        return Response({
            'success': False,
            'message': self.error_messages[message_key],
            'user_id': None,
        }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        user = None
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        if email :
            try:
                user = authenticate(email=email, password=password)
            except ObjectDoesNotExist:
                pass
        
        if not user:
            user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'success': True,
                'message': "Login successful",
                'token': token.key,
                'user_id': user.id,
            }, status=status.HTTP_200_OK)
        else:
            return self._error_response('disabled')


# Use this class for logout 
class UserLogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            # delete the user's token
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            # Token does not exist, user is effectively logged out already
            raise NotFound(detail='Token not found - User is not aunthenticate', code=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            # Handle other exceptions (e.g., database errors) appropriately
            return Response({'error': 'An error occurred during logout.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)