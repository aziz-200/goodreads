from rest_framework import serializers
from books.models import Book, BookReview
from users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'username', 'email')

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'isbn')

class BookReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='user')
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source='book')

    class Meta:
        model = BookReview
        fields = ('id', 'stars_given', 'comment', 'user', 'book', 'user_id', 'book_id')