from django.core.paginator import Paginator
from django.shortcuts import render

from books.models import BookReview


def landing(request):
    return render(request, 'landing.html')


def home(request):
    book_reviews = BookReview.objects.all().order_by('-created_at')
    page_size = request.GET.get('page_size', 4)  # Lowered to 4 for testing visual pagination easily
    paginator = Paginator(book_reviews, page_size)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # PASS page_obj TO THE TEMPLATE CONTEXT
    return render(request, 'home.html', {'page_obj': page_obj})
