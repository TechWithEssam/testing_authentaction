from django.urls import path, include
from . import views


app_name = "accounts"
urlpatterns = [
    path("account/<username>/", views.profile_view, name="profile"),
    path("signup/", views.register_view, name="register"),
    path("verify/", views.verify, name="verify"),
    path("signin/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
