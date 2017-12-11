from django.db import models
from shoping.apps.product.models import Product


class Status(models.Model):
    ACCEPTED = 1
    REJECTE = 2
    PENDING = 3
    FAILED = 4

    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Status'

    def __str__(self):
        return self.name

class ProductQuantity(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return 'product({}): {} | quantity: {} | subtotal: {}'.format(
            self.product.pk if self.product else '',
            self.product.name if self.product else '',
            self.quantity,
            self.subtotal
        )


class Ticket(models.Model):
    items = models.ManyToManyField(ProductQuantity)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.ForeignKey(Status, models.PROTECT)

    def save(self, *args, **kwargs):
        if self.pk and self.items:
            self.total = sum([item.product.subtotal for item in self.items.all()])
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.pk)
