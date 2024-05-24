from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ...models import Books
from ...serializers import BooksSerializer
from rest_framework.authentication import get_authorization_header
from ...authentication import decode_access_token

def authentication(request):
    auth = get_authorization_header(request).split()
    
    if not auth or len(auth) != 2:
        return Response({"error": "Token não encontrado"}, status=status.HTTP_401_UNAUTHORIZED)

    token = auth[1].decode('utf-8')
    valid_token = decode_access_token(token)
    
    if not valid_token:
        return Response({"error": "Token inválido"}, status=status.HTTP_401_UNAUTHORIZED)
    
    return valid_token

class BooksAPI(generics.ListCreateAPIView):
    
    serializer_class = BooksSerializer
    
    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'book_category': openapi.Schema(type=openapi.TYPE_STRING),
                'book_name': openapi.Schema(type=openapi.TYPE_STRING),
                'book_description': openapi.Schema(type=openapi.TYPE_STRING),
                'book_release_year': openapi.Schema(type=openapi.TYPE_INTEGER),
                'book_price': openapi.Schema(type=openapi.TYPE_NUMBER),
            }
        ),
        responses={
            201: 'Created',
            400: 'Bad Request',
            401: 'Unauthorized',
            500: 'Internal Server Error'
        }
    )
    @api_view(['POST'])
    def create_books(request):
        """
        Create a new book.
        """
        auth_response = authentication(request)
        if isinstance(auth_response, Response):
            return auth_response

        try:
            book_data = {
                "book_category": request.data.get('book_category'),
                "book_name": request.data.get('book_name'),
                "book_description": request.data.get('book_description'),
                "book_release_year": request.data.get('book_release_year'),
                "book_price": request.data.get('book_price')
            }

            book = Books(**book_data)
            book.save()
            serializer = BooksSerializer(book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        method='get',
        responses={
            200: 'OK',
            401: 'Unauthorized',
            500: 'Internal Server Error'
        }
    )
    @api_view(['GET'])
    def get_books(request):
        """
        Get all books.
        """
        auth_response = authentication(request)
        if isinstance(auth_response, Response):
            return auth_response

        try:
            books = Books.objects.all()
            serializer = BooksSerializer(books, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        method='put',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING),
                'book_category': openapi.Schema(type=openapi.TYPE_STRING),
                'book_name': openapi.Schema(type=openapi.TYPE_STRING),
                'book_description': openapi.Schema(type=openapi.TYPE_STRING),
                'book_release_year': openapi.Schema(type=openapi.TYPE_INTEGER),
                'book_price': openapi.Schema(type=openapi.TYPE_NUMBER),
            }
        ),
        responses={
            200: 'OK',
            401: 'Unauthorized',
            500: 'Internal Server Error'
        }
    )
    @api_view(['PUT'])
    def update_books(request):
        """
        Update a book.
        """
        auth_response = authentication(request)
        if isinstance(auth_response, Response):
            return auth_response

        try:
            book_id = request.data.get('id')
            book = Books.objects.get(id=book_id)
            book.book_category = request.data.get('book_category', book.book_category)
            book.book_name = request.data.get('book_name', book.book_name)
            book.book_description = request.data.get('book_description', book.book_description)
            book.book_release_year = request.data.get('book_release_year', book.book_release_year)
            book.book_price = request.data.get('book_price', book.book_price)

            book.save()
            serializer = BooksSerializer(book)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        method='delete',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            204: 'No Content',
            401: 'Unauthorized',
            500: 'Internal Server Error'
        }
    )
    @api_view(['DELETE'])
    def delete_book(request):
        """
        Delete a book.
        """
        auth_response = authentication(request)
        if isinstance(auth_response, Response):
            return auth_response

        book_id = request.data.get('id')
        try:
            book = Books.objects.get(id=book_id)
            book.delete()
            return Response({"message": 'successfully deleted book'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
