from rest_framework.routers import DefaultRouter
from .views import CommentViewSet
from django.urls import include, path

router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls))
]
