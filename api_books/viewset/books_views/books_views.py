from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ...models import Books
from ...serializers import BooksSerializer

@api_view(['GET'])
def get_books(request):
    try:
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
