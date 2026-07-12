from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from books.models import BookReview, Book
from .serializers import BookReviewSerializer
from rest_framework import viewsets

# class BookReviewViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = BookReview.objects.all()
#     serializer_class = BookReviewSerializer
#     lookup_field = 'id'
#





class BookReviewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        book_review = get_object_or_404(BookReview, id=id)
        serializer = BookReviewSerializer(book_review)
        return Response(data=serializer.data)

    def delete(self, request, id):
        book_review = get_object_or_404(BookReview, id=id)
        book_review.delete()
        return Response(status=204)

    def put(self, request, id):
        book_review = get_object_or_404(BookReview, id=id)
        serializer = BookReviewSerializer(book_review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(serializer.errors, status=400)

class BookReviewListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        book_reviews = BookReview.objects.all().order_by('-id')
        paginator = PageNumberPagination()
        page_obj = paginator.paginate_queryset(book_reviews, request)
        serializer = BookReviewSerializer(page_obj, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = BookReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=201)
        return Response(serializer.errors, status=400)