from django.urls import path
from .views import MyChatsView

app_name = "chat"

urlpatterns = [
    path('my-chats/', MyChatsView.as_view(), name='my_chats'),
    path('chat-with/<str:id>', MyChatsView.as_view(), name='chat-with'),
]