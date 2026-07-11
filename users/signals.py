from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save

from users.models import CustomUser
from users.tasks import send_email


@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
        print(f"created: {created}")
        if created:
            print("created")
            send_email.delay(
                'Welcome to GoodReads',
                f"Hi, {instance.username}! Welcome to GoodReads.",
                [instance.email]
            )