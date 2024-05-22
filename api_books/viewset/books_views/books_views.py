from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
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

@api_view(['POST'])
def get_books(request):
    auth_response = authentication(request)
    if isinstance(auth_response, Response):
        return auth_response

    try:
        books = Books.objects.all()
        serializer = BooksSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def create_books(request):
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

@api_view(['PUT'])
def update_books(request):
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

@api_view(['DELETE'])
def delete_book(request):
    auth_response = authentication(request)
    if isinstance(auth_response, Response):
        return auth_response

    book_id = request.data.get('id')
    try:
        book = Books.objects.get(id=book_id)
        book.delete()
        return Response({"message": 'successfully deleted book', "status": status.HTTP_204_NO_CONTENT})
    except Exception as e:
        return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
