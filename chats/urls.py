from django.urls import path
from . import views


app_name = "chats"

urlpatterns = [
    path("direct/chats/", views.my_chat_view, name="my_chat"),
    path("dir/<slug>/", views.prived_message_view, name="prived_message"),
    path("contact/", views.contact_buyer_view, name="contact_salesman"),
    # path("send-message/", views.send_message_view, name="send_message")
]