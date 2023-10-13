from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import MyUser
from .serializers import MyUserSerializer
from django.shortcuts import get_list_or_404


@api_view(['GET', 'POST'])
def user_list(request):
    """
    List all users, or create a new user.
    """
    if request.method == 'GET':
        users = get_list_or_404(MyUser)
        serializer = MyUserSerializer(users, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = MyUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, uuid):
    """
    Retrieve, update or delete a user.
    """
    user = get_object_or_404(MyUser, pk=uuid)

    if request.method == 'GET':
        serializer = MyUserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MyUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)