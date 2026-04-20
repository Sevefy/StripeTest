from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(verbose_name="Название", max_length=256)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    price = models.DecimalField(verbose_name="Цена",  max_digits=12, decimal_places=2)
    class Meta:
        ordering = ['-price']
        constraints = [
            models.CheckConstraint(condition=models.Q(price__gte=0), name="price_gte_18"),
        ]
        indexes = [
            models.Index(fields=["name"], name="name_idx")
        ]
    