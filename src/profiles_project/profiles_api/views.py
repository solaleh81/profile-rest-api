from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import HelloSerializers, UserProfileSerializer, ProfileFeedItemSerializer
from rest_framework import serializers, status, viewsets, filters
from .models import UserProfile, ProfileFeedItem
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from . import permissions
from django.db.models import Q
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

class HelloApiView(APIView):
    """
    Test Api View.
    """

    serializer_class = HelloSerializers

    def get(self, request, format=None):
        """
        Returns a list of ApiView features.
        """
        an_apiview = [
            'test',
            'test2'
        ]
        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """
        Creates a hello post with our name.
        """

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        return Response({'method': 'put'})

    def patch(self, request, pk=None):
        return Response({'method': 'patch'})

    def delete(self, request, pk=None):
        return Response({'method': 'delete'})


class HelloViewSet(viewsets.ViewSet):

    serializer_class = HelloSerializers
    def list(self, request):

        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to urls using Routers.',
            'provides more functionality with less code.'
        ]
        return Response({'list': a_viewset})

    def create(self, request):
        """
        Create a new hello message.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.data.get('name')
        message = 'Hello {0}'.format(name)
        return Response({'message': message})

    def retrieve(self, request, pk=None):
        """
        Retrieve an object with its ID.
        """
        return Response({'http_method': 'GET'})


    def update(self, request, pk=None):
        """
        Handles updating an object with its ID.
        """
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """
        Handles partial updating an object with its ID.
        """
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """
        Handles destroying an object with its ID.
        """
        return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    Handles creating and updating profiles.
    """
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', 'email',)


    def filter_queryset(self, queryset):
        """
        Override filter queryset to use q instead of search.
        """
        queryset = super().filter_queryset(queryset)
        search_param = self.request.query_params.get('q')
        if search_param:
            queryset = queryset.filter(
                Q(name__icontains=search_param) |
                Q(email__icontains=search_param)
            )
        return queryset


class LoginViewSet(viewsets.ViewSet):
    """
    checks email and password and return an auth token.
    """
    serializer_class = AuthTokenSerializer

    def create(self, request):
        """
        Use the ObtainAuthToken ApiView to validate and create a token.
        """
        return ObtainAuthToken().as_view()(request=request._request)

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """
    Handles reading, creating and updating profile feed items.
    """
    serializer_class = ProfileFeedItemSerializer
    queryset = ProfileFeedItem.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated, permissions.PostOwnStatus]

    def perform_create(self, serializer):
        """
        sets the user profile to the logged in user.
        """
        serializer.save(user_profile=self.request.user)
