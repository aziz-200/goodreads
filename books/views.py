from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import paginator
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from .forms import BookReviewForm
from .models import Book, BookReview
from django.db.models import Q


# class BooksView(ListView):
#     template_name = 'books/list.html'
#     queryset = Book.objects.all()
#     context_object_name = 'books'
#     ordering = ['-id'] # oxirgi qo'shilgani birinchi ko'rinadi
#     paginate_by = 4 bu yerda bir qator kod orqali qilinadi

    #tepadagi bilan bir xil

class BooksView(View):
    def get(self, request):
        books = Book.objects.all().order_by('-id')
        search_query = request.GET.get('search')
        # Search by title, description, or ISBN
        if search_query:
            books = books.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(isbn__icontains=search_query)
            )

        paginator = Paginator(books, 4)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)
        return render(request, 'books/list.html', {'books': page_obj, 'page_obj': page_obj})


#
# class BookDetailView(DetailView):
#     template_name = 'books/detail.html'
#     pk_url_kwarg = 'id'
#     model = Book
#
# #

class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm()
        return render(request, "books/detail.html",
                      {'book': book,
                       'review_form': review_form})


class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm(data=request.POST)

        if review_form.is_valid():
            BookReview.objects.create(
                book=book,
                user=request.user,
                stars_given=review_form.cleaned_data['stars_given'],
                comment=review_form.cleaned_data['comment']
            )
            return redirect(reverse("books:detail", kwargs={"id": book.id}))

        return render(request, "books/detail.html", {
            'book': book,
            'review_form': review_form
        })