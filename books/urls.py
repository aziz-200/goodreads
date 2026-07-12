from django.urls import path
from .views import BooksView, BookDetailView, AddReviewView, EditReviewView, DeleteReviewView, ConfirmDeleteReviewView

app_name = 'books'
urlpatterns = [
    path('', BooksView.as_view(), name='list'),
    path('<int:id>/', BookDetailView.as_view(), name='detail'),
    path('<int:id>/reviews/', AddReviewView.as_view(), name='review'),
    path('<int:bookid>/reviews/<int:reviewId>/edit/', EditReviewView.as_view(), name='edit-review'),
    path('<int:bookid>/reviews/<int:reviewId>/delete/confirm/', ConfirmDeleteReviewView.as_view(), name='delete-confirm-review'),
    path('<int:bookid>/reviews/<int:reviewId>/delete/', DeleteReviewView.as_view(), name='delete-review'),
]