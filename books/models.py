import code
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from users.models import CustomUser


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=5000)
    isbn = models.IntegerField()
    cover_picture = models.ImageField(upload_to='cover_pic', blank=True, default='cover_default_pic.jpg')
    def __str__(self):
        return self.title

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class BookAuthor(models.Model): # many to many relationship uchun tableni yaratish maqsadida kk
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    @property
    def full_name(self):
        return f"{self.author.first_name} {self.author.last_name}"

    def __str__(self):
        return f'{self.book.title} {self.author.first_name} {self.author.last_name}'

class BookReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.TextField()
    stars_given = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f'{self.stars_given} by {self.user.first_name}'
