from django.urls import path
from .views import host_image, ImageView, ListImageView

from rest_framework import routers

router = routers.DefaultRouter()

# url patterns for the hostimage app

urlpatterns = [
    path('', host_image),
    path('uploadimage/', ImageView.as_view(), name='image-upload'),
    path('listimages/', ListImageView.as_view(), name='image-list'),   
]
