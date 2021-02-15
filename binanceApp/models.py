from django.db import models
# Create your models here.


class Order(models.Model):
    order = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    range_price = models.DecimalField(max_digits=10, decimal_places=2, unique=True)
    btc_count = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    order_id = models.IntegerField(default=None)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)