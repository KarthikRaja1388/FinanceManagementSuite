from django.db import models
from django.conf import settings

# Create your models here.
class Account(models.Model):
    account_name = models.CharField(max_length=100)
    current_balance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_primary = models.BooleanField(default=False)
    account_admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        existing_accounts = Account.objects.filter(account_admin = self.account_admin).exclude(id=self.id)

        if not existing_accounts.exists():
            self.is_primary = True
        elif self.is_primary:
            existing_accounts.update(is_primary=False)

        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['account_name', 'account_admin'],
                name='unique_account_name_per_user'
            )
        ]


    def __str__(self):
        return self.account_name