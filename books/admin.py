from django.contrib import admin
from books.models import (Book,
                          Author,
                          BookAuthor,
                          BookReview)


class BookAdmin(admin.ModelAdmin):
    search_fields = ["title", 'isbn']
    # list_filter = ['title',"isbn"] bu yerda kk emas ammo filter qilish uchun ishlatiladi
    list_display = ['title', 'isbn']

class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']
    list_display = ['first_name', 'last_name']

class BookAuthorAdmin(admin.ModelAdmin):
    search_fields = ["book", 'author']
    list_display = ['book', 'author']
    list_filter = ['book', 'author']

class BookReviewAdmin(admin.ModelAdmin):
    search_fields = ['stars_given']
    list_display = ['stars_given', 'book']
    list_filter = ['stars_given']



admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(BookReview, BookReviewAdmin)
