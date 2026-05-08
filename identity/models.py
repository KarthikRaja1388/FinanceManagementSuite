from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    class UserType(models.TextChoices):
        ADMIN = 'ADM'
        EDITOR = 'EDI'
        VIEW = 'VIE'

    user_type = models.CharField(
        max_length=3,
        choices=UserType.choices,
        default='VIE'
    )
    account_owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owner'
    )
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_type