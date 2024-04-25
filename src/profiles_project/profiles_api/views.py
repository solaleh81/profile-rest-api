from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


class HelloApiView(APIView):
    """
    Test Api View.
    """

    def get(self, request, format=None):
        """
        Returns a list of ApiView features.
        """
        an_apiview = [
            'test',
            'test2'
        ]
        return Response({'message': 'Hello!', 'an_apiview': an_apiview})
    