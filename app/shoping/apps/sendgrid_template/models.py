from django.db import models


class Sendgrid(models.Model):

    NAME_CHOICES = (
        ('register', 'Register'),
        ('newsletter', 'Newsletter'),
        ('purchase', 'Purchase'),
    )

    name = models.CharField(
        max_length=15,
        choices=NAME_CHOICES,
        unique=True,
    )

    category = models.CharField(
        blank=True,
        max_length=255,
    )

    template_id = models.CharField(
        max_length=255,
    )

    def __str__(self):
        return self.name
