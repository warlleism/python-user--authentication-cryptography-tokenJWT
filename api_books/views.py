# File path: views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Books
from .serializers import UserSerializer, BooksSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import bcrypt


@api_view(['POST'])
def register_user(request):
    try:
        user_email = request.data.get('user_email')
        user_password = request.data.get('user_password')

        if not user_email or not user_password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), salt)

        user_data = {
            "user_email": user_email,
            "user_password": hashed_password.decode('utf-8'),
        }

        user = User(**user_data)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except:
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def login_user(request):
    try:
        user_email = request.data.get('user_email')
        user_password = request.data.get('user_password')

        if not user_email or not user_password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(user_email=user_email)

        if bcrypt.checkpw(user_password.encode('utf-8'), user.user_password.encode('utf-8')):
            refresh = RefreshToken.for_user(user)
            return Response({"status": 200, "token": str(refresh.access_token), "message": "User authenticated."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
def remove_user(request):
    try:
        id = request.data.get('id')
        
        if not id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=id)
        user.delete()

        return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

       
