from django.db import models
from django.conf import settings

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=50, default="fa-circle")
    is_system = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['category_name', 'user'],
                name='unique_category_per_user'
            )
        ]

    def __str__(self):
        return self.category_name