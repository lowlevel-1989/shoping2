from django.db import models


class EpayCo(models.Model):

    COP = 'COP'
    USD = 'USD'

    CURRENCY_CHOICES = (
        (COP, COP),
        (USD, USD),
    )

    client_id = models.CharField(max_length=10)
    p_key = models.CharField(max_length=40)
    p_currency_code = models.CharField(
            blank=False,
            max_length=3,
            choices=CURRENCY_CHOICES,
            default=COP,
    )
    test = models.BooleanField(default=True)
    url_response = models.URLField()
    url_confirmation = models.URLField()

    class Meta:
        verbose_name = 'EpayCo'
        verbose_name_plural = 'EpayCo'

    def __str__(self):
        return self.client_id
