from django.test import TestCase
from django.urls import reverse
from books.models import Book
from users.models import CustomUser


class BooksTest(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse('books:list'))
        self.assertContains(response, 'Our shelves are currently empty')

    def test_books_list(self):
        book1 = Book.objects.create(title='book1', isbn='313451', description='description1')
        book2 = Book.objects.create(title='book2', isbn='123451', description='description2')
        book3 = Book.objects.create(title='book3', isbn='123234', description='description3')
        book4 = Book.objects.create(title='book4', isbn='123234', description='description3')
        book5 = Book.objects.create(title='book5', isbn='123234', description='description3')
        book6 = Book.objects.create(title='book6', isbn='123234', description='description3')
        response_page1 = self.client.get(reverse('books:list'))

        for book in [book6, book5, book4, book3]:
            self.assertContains(response_page1, book.title)
        self.assertNotContains(response_page1, book1.title)
        self.assertNotContains(response_page1, book2.title)
        response_page2 = self.client.get(reverse('books:list') + '?page=2')

        for book in [book2, book1]:
            self.assertContains(response_page2, book.title)

    def test_book_detail(self):
        book = Book.objects.create(title='book1', isbn='313451', description='description1')
        response = self.client.get(reverse('books:detail', kwargs={'id': book.id}))
        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_search(self):
        book1 = Book.objects.create(title='book1', isbn='313451', description='description1')
        book2 = Book.objects.create(title='book2', isbn='123451', description='description2')
        response = self.client.get(reverse('books:list') + '?search=book1')
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)


def test_add_review(self):
    book = Book.objects.create(title='book1', isbn=313451, description='description1')

    user = CustomUser.objects.create(
        username='test1',
        first_name='test1',
        last_name='test1',
        email='blabla@gmail.com'
    )
    user.set_password('1234')
    user.save()

    self.client.login(username='test1', password='1234')

    response = self.client.post(
        reverse('books:review', kwargs={'id': book.id}),
        data={
            'stars_given': 5,
            'comment': 'test comment',
        }
    )
    book_reviews = book.bookreview_set.all()

    self.assertEqual(response.status_code, 302)
    self.assertEqual(book_reviews.count(), 1)
    self.assertEqual(book_reviews.first().comment, 'test comment')
    self.assertEqual(book_reviews.first().stars_given, 5)

