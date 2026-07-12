import code
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
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


class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, bookid, reviewId):
        book = Book.objects.get(id=bookid)
        review = book.bookreview_set.get(id=reviewId)
        review_form = BookReviewForm(instance=review)
        return render(request, "books/edit_review.html", {
            'book': book,
            'review': review,
            'review_form': review_form
        })
    def post(self, request, bookid, reviewId):
        book = Book.objects.get(id=bookid)
        review = book.bookreview_set.get(id=reviewId)
        review_form = BookReviewForm(data=request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()
            return redirect(reverse("books:detail", kwargs={"id": book.id}))

class ConfirmDeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, bookid, reviewId):
        book = Book.objects.get(id=bookid)
        review = book.bookreview_set.get(id=reviewId)
        return render(request, 'books/confirm_delete_review.html', {'book': book, 'review': review})

class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, bookid, reviewId):
        book = Book.objects.get(id=bookid)
        review = book.bookreview_set.get(id=reviewId)

        review.delete()
        messages.success(request, "Review deleted successfully")
        return redirect(reverse("books:detail", kwargs={"id": book.id}))
