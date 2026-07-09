from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import  reverse
from django.contrib.auth import get_user

class RegisterationTest(TestCase):
    def test_user_account_is_created(self):
        self.client.post(reverse("users:register"),
                         data = {
                             'username': 'test1',
                             'first_name': 'test2',
                             'last_name': 'test3',
                             'email': 'test@gmail.com',
                             'password': 'aziz02010815',
                         }, format='json')
        user = User.objects.get(username='test1')

        self.assertEqual(user.first_name, 'test2')
        self.assertEqual(user.last_name, 'test3')
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertNotEqual(user.password, '   aziz02010815')
        self.assertTrue(user.check_password('aziz02010815'))

    def test_requirment_fields(self):
        response = self.client.post(reverse("users:register"),
                         data={
                             'first_name': 'test1',
                             'last_name': 'test2',
                             'email': 'test2@gmail.com',
                         })

        self.assertEqual(User.objects.count(), 0)

        form = response.context['form']

        self.assertFormError(form, 'username', 'This field is required.')
        self.assertFormError(form , 'password', 'This field is required.')

    def test_valid_email(self):
        response = self.client.post(reverse("users:register"),
                         data={
                             'username': 'test1',
                             'first_name': 'test2',
                             'last_name': 'test3',
                             'email': 'test gmail.com',
                             'password': 'aziz02010815',
                         }, format='json')
        form = response.context['form']
        user_account = User.objects.count()
        self.assertEqual(user_account, 0)
        self.assertFormError(form, 'email', 'Enter a valid email address.')

    def test_unique_username(self):

        user = User.objects.create_user(username='test1',
                                        first_name='test2')
        user.set_password('password')
        user.save()

        response = self.client.post(reverse("users:register"),
                         data={
                             'username': 'test1',
                             'first_name': 'test2',
                             'last_name': 'test3',
                             'email': 'test@gmail.com',
                             'password': 'aziz02010815',
                         }, format='json')
        form = response.context['form']

        user_account = User.objects.count()
        self.assertEqual(user_account, 1)
        self.assertFormError(form, 'username', 'A user with that username already exists.')


class LoginTest(TestCase):
    def test_successful_login(self):
        User.objects.create_user(username='test1', password='qw1221', first_name='test1', last_name='test1')

        response = self.client.post(
            reverse("users:login"),
            data={
                'username': 'test1',
                'password': 'qw1221',
            }
        )

        self.assertEqual(response.status_code, 302)
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.username, 'test1')

    def test_wrong_credentials(self):
        User.objects.create_user(username='test1', password='qw1221', first_name='test1', last_name='test1')

        response = self.client.post(
            reverse("users:login"),
            data={
                'username': 'wrong_user',
                'password': 'qw1221',
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        response = self.client.post(
            reverse("users:login"),
            data={
                'username': 'test1',
                'password': 'wrong',
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

