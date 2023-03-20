from django.urls import path
from . import views
app_name = "products"
urlpatterns = [
    path('', views.home_product, name="home"),
    path('not-found/', views.not_found_view, name="not_found"),
    path('upload-product/', views.upload_product_view, name="upload_product"),
    path("detail/<slug>/", views.detail_product_view, name="detail_product"),
]