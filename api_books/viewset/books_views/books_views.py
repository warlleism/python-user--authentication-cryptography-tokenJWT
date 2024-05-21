from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ...models import Books
from ...serializers import BooksSerializer
from rest_framework.authentication import get_authorization_header
from ...authentication import decode_access_token
from rest_framework.exceptions import AuthenticationFailed


@api_view(['POST'])
def get_books(request):

    try:
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)
            books = Books.objects.all()
            serializer = BooksSerializer(books, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    except Exception as e:
        return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_books(request):
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
