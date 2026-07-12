from api.views import BookReviewAPIView, BookReviewListAPIView, BookReviewViewSet
from django.urls import path
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('reviews', BookReviewViewSet, basename="review")


app_name = 'api'

urlpatterns = router.urls

# urlpatterns = [
#     path('reviews/<int:id>', BookReviewAPIView.as_view(), name='book-review-detail'),
#     path('reviews/', BookReviewListAPIView.as_view(), name='book-review-list')
# ]