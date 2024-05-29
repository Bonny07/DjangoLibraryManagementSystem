from rest_framework import serializers
from .models import Author, Book, BorrowRecord


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name']


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date']


class BorrowRecordSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = BorrowRecord
        fields = ['book', 'borrower', 'borrow_date', 'return_date']
