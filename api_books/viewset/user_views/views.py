from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from ...models import User
from ...serializers import UserSerializer
from ...authentication import create_access_token, create_refresh_token
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import bcrypt


class API(generics.ListCreateAPIView):

    serializer_class = UserSerializer

    @staticmethod
    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_email': openapi.Schema(type=openapi.TYPE_STRING),
                'user_password': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            201: 'Created',
            400: 'Bad Request',
            500: 'Internal Server Error'
        }
    )
    @api_view(['POST'])
    def register_user(request):
        try:
            user_email = request.data.get('user_email')
            user_password = request.data.get('user_password')

            if not user_email or not user_password:
                return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(
                user_password.encode('utf-8'), salt)

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

    @staticmethod
    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_email': openapi.Schema(type=openapi.TYPE_STRING),
                'user_password': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: 'OK',
            400: 'Bad Request',
            401: 'Unauthorized',
            500: 'Internal Server Error'
        }
    )
    @api_view(['POST'])
    def login_user(request):
        try:
            user_email = request.data.get('user_email')
            user_password = request.data.get('user_password')

            if not user_email or not user_password:
                return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(user_email=user_email)

            if bcrypt.checkpw(user_password.encode('utf-8'), user.user_password.encode('utf-8')):
                user = User.objects.get(user_email=user_email)
                serializer = UserSerializer(user)
                access_token = create_access_token(serializer.data['id'])
                refresh_token = create_refresh_token(serializer.data['id'])
                response = Response()
                response.set_cookie(key='refresh_token',
                                    value=refresh_token, httponly=True)
                response.data = {'token': access_token}

                return response
            else:
                return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    @swagger_auto_schema(
        method='delete',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: 'OK',
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        }
    )
    @api_view(['DELETE'])
    def remove_user(request):
        try:
            user_id = request.data.get('id')

            if not user_id:
                return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(id=user_id)
            user.delete()

            return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
