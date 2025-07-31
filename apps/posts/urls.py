from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostViewSets

router = DefaultRouter()
router.register(r'posts', PostViewSets, basename='post')

urlpatterns = [
    path('', include(router.urls))
]

