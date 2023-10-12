from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User


@api_view(['GET'])
def current_user(request):
    print(request.user)
    return Response({'username': request.user.username})


class Signup(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        # CREATING USER
        if not request.data['username'] or not request.data['password']:
            return Response({'error': 'Field may not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username = request.data['username']).exists():
            return Response({'Error': "A user with this username already exists"},status=status.HTTP_400_BAD_REQUEST)
        new_user = User(username = request.data['username'])
        new_user.set_password(request.data['password'])
        new_user.save()
        
        return Response(status=status.HTTP_200_OK)
        