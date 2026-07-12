from django.urls import reverse
from rest_framework.test import APITestCase

from books.models import Book, BookReview
from users.models import CustomUser


class BookReviewAPITest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', first_name='testName')
        self.user.set_password('testpassword')
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_book_review_detail(self):
        book = Book.objects.create(title='book1', isbn=313451, description='description1')
        br = BookReview.objects.create(user=self.user, book=book, stars_given=5, comment='comment1')

        response = self.client.get(reverse('api:book-review-detail', kwargs={'id': br.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], br.id)
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['comment'], 'comment1')
        self.assertEqual(response.data['book']['id'], book.id)
        self.assertEqual(response.data['book']['title'], book.title)
        self.assertEqual(response.data['book']['description'], book.description)
        self.assertEqual(response.data['book']['isbn'], book.isbn)
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['first_name'], self.user.first_name)
        self.assertEqual(response.data['user']['username'], self.user.username)

    def test_book_review_list(self):
        book = Book.objects.create(title='book1', isbn=313451, description='description1')
        br1 = BookReview.objects.create(user=self.user, book=book, stars_given=5, comment='comment1')
        br2 = BookReview.objects.create(user=self.user, book=book, stars_given=4, comment='comment2')
        user2 = CustomUser.objects.create_user(username='testuser2', first_name='testName2')
        response = self.client.get(reverse('api:book-review-list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(
            response.data['results'][0]['id'], br2.id
        )

    def test_delete_review(self):
        book = Book.objects.create(title='book1', isbn=313451, description='description1')
        br = BookReview.objects.create(user=self.user, book=book, stars_given=5, comment='comment1')
        response = self.client.delete(reverse('api:book-review-detail', kwargs={'id': br.id}))
        self.assertEqual(response.status_code, 204)

    def test_create_review(self):
        book = Book.objects.create(title='book1', isbn=313451, description='description1')
        data = {
            'stars_given': 4,
            'comment': 'New comment',
            'book_id': book.id,
            'user_id': self.user.id
        }
        response = self.client.post(reverse('api:book-review-list'), data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BookReview.objects.count(), 1)
        self.assertEqual(BookReview.objects.first().comment, 'New comment')

    def test_update_review(self):
        book = Book.objects.create(title='book1', isbn=313451, description='description1')
        br = BookReview.objects.create(user=self.user, book=book, stars_given=5, comment='comment1')
        data = {
            'stars_given': 3,
            'comment': 'Updated comment',
            'book_id': book.id,
            'user_id': self.user.id
        }
        response = self.client.put(reverse('api:book-review-detail', kwargs={'id': br.id}), data=data)
        self.assertEqual(response.status_code, 200)
        br.refresh_from_db()
        self.assertEqual(br.stars_given, 3)
        self.assertEqual(br.comment, 'Updated comment')

    def test_invalid_create_review(self):
        data = {
            'stars_given': 4,
            'comment': 'New comment',
            'book_id': 9999,
            'user_id': self.user.id
        }
        response = self.client.post(reverse('api:book-review-list'), data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('book_id', response.data)
        