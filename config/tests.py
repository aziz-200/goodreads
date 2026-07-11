from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookReview
from users.models import CustomUser


class HomePageTest(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title='book1', isbn=313451, description='description1')

        user = CustomUser.objects.create(username='testuser', first_name='testuser', last_name='testuser', email='')
        user.set_password('1234')
        user.save()

        review1 = BookReview.objects.create(user=user, book=book, stars_given=5, comment='comment1')
        review2 = BookReview.objects.create(user=user, book=book, stars_given=4, comment='comment2')
        review3 = BookReview.objects.create(user=user, book=book, stars_given=3, comment='comment2')
        review4 = BookReview.objects.create(user=user, book=book, stars_given=1, comment='comment2')
        review5 = BookReview.objects.create(user=user, book=book, stars_given=5, comment='comment2')
        review6 = BookReview.objects.create(user=user, book=book, stars_given=3, comment='comment2')
        review7 = BookReview.objects.create(user=user, book=book, stars_given=4, comment='comment2')

        review8 = BookReview.objects.create(user=user, book=book, stars_given=2, comment='who is the cary the boat')
        review9 = BookReview.objects.create(user=user, book=book, stars_given=5, comment='who is the cary the boat')

        response = self.client.get(reverse('home') + '?page_size=2')

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'who is the cary the boat')

        response_page_2 = self.client.get(reverse('home') + '?page_size=2&page=2')
        self.assertContains(response_page_2, 'comment2')