from django.urls import path
from . import views
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')
router.register('profile', views.UserProfileViewSet, basename='userprofile')

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view(), name='test'),
    path('', include(router.urls)),
]
