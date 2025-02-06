from django.urls import path
from . import views
from . import consumers

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('ws/chat/', consumers.ChatConsumer.as_asgi()),  # Replace `chat_view` with your actual view function
]
