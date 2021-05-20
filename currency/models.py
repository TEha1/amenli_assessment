from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UserCurrency(models.Model):
    USD = 'USD'
    EUR = 'EUR'
    EGP = 'EGP'

    CURRENCY_CHOICES = (
        (USD, 'USD'),
        (EUR, 'EUR'),
        (EGP, 'EGP'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_currencies",
        verbose_name="user",
    )
    from_currency_type = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        verbose_name="from currency type"
    )
    to_currency_type = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        verbose_name="to currency type"
    )
    times = models.PositiveIntegerField(
        default=1,
        verbose_name="times"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="creation date"
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name="modification date"
    )

    class Meta:
        verbose_name = "User Currency"
        verbose_name_plural = "User Currencies"

    def __str__(self):
        return f'{self.user} - {self.times}'
