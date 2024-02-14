#from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Profile
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView  # for logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import render, redirect
from .forms import LoginForm, UpdateProfileForm

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
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login_test.html'

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

    def get(self, request):
        #form = LoginForm() # this way is for render()
        #return render(request, 'login_test.html', {'form': form})
        profile = Profile.objects.all()
        serializer = UserLoginSerializer()
        return Response({'serializer': serializer, 'profile': profile})

    def post(self, request, *args, **kwargs):
        user = None
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        # print("Received POST request for user login")
        # print("Username:", username)
        # print("Email:", email)
        if email :
            try:
                user = authenticate(email=email, password=password)
            except ObjectDoesNotExist:
                pass
        
        if not user:
            user = authenticate(username=username, password=password)
            
        if user:
            login(request, user)  # Log in the user
            token, _ = Token.objects.get_or_create(user=user)
            request.session['auth_token'] = token.key
            #print(token)  
            return redirect('user:profile')
            # return Response({
            #     'success': True,
            #     'message': "Login successful",
            #     'token': token.key,
            #     'user_id': user.id,
            # }, status=status.HTTP_200_OK)
        else:
            return self._error_response('disabled')
        

#TODO:add html
# Use this class for logout 
class UserLogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            # delete the user's token
            token = Token.objects.get(user=request.user)
            #print(Token.objects.get(user=request.user))
            token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            # Token does not exist, user is effectively logged out already
            raise NotFound(detail='Token not found - User is not aunthenticate', code=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            # Handle other exceptions (e.g., database errors) appropriately
            return Response({'error': 'An error occurred during logout.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# Class is specified in the request get for profile page
class ProfileView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile.html'

    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            user = request.user  # Get the authenticated user
            #print(user.profile.avatar)
            profile_data = {
                'username': user.username,
                'email': user.email,
                'bio': user.profile.bio,
                'avatar': user.profile.avatar
            }
            print(Token.objects.get(user=request.user))
            return Response(profile_data)
        except Token.DoesNotExist:
            # Token does not exist, user is effectively logged out already
            raise NotFound(detail='Token not found - User is not aunthenticate', code=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            # Handle other exceptions (e.g., database errors) appropriately
            return Response({'error': 'An error occurred during logout.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Class is specified in the request get/post for update profile page
class ProfileUpdateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            profile_form = UpdateProfileForm(instance=request.user.profile)
            return render(request, 'update_profile.html', {'form': profile_form})
        except Token.DoesNotExist:
            # Token does not exist, user is effectively logged out already
            raise NotFound(detail='Token not found - User is not aunthenticate', code=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            # Handle other exceptions (e.g., database errors) appropriately
            print(e)
            return Response({'error': 'An error occurred during profile update.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='user:profile')