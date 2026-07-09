from django.test import TestCase
from django.urls import reverse

from books.models import Book


class BooksTest(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse('books:list'))

        self.assertContains(response, 'No books found')

    def test_books_list(self):
        Book.objects.create(title='book1',  isbn='313451', description='description1')
        Book.objects.create(title='book2',  isbn='123451', description='description2')
        Book.objects.create(title='book3',  isbn='123234', description='description3')

        response = self.client.get(reverse('books:list'))
        books = Book.objects.all()
        for book in books:
            self.assertContains(response, book.title)

    def test_book_detail(self):
        book = Book.objects.create(title='book1', isbn='313451', description='description1')
        response = self.client.get(reverse('books:detail', kwargs={'id':book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)