from django.db import models


class ItemModel(models.Model):

    title = models.CharField(verbose_name='Название', max_length=40)
    price = models.DecimalField(verbose_name='Цена', max_digits=9, decimal_places=2)

    def __str__(self):
        return self.title
