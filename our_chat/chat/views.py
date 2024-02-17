from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import status
from user.models import Friend
from django.db.models import Q

# Class with all defined friends(contacts)
class MyChatsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name ='my_chats.html'

    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        try:
            user = request.user  
            #friends = Friend.objects.filter(Q(profile_one=user.profile) | Q(profile_two=user.profile))
            friends = Friend.objects.filter(Q(profile_one=user.profile))
            friend_data = []
            for friend in friends:
                friend_data.append(friend)
            return Response({'friends': friend_data})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)