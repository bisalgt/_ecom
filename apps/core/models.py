from django.db import models
from django.conf import settings
from django.shortcuts import reverse


class Item(models.Model):
    title = models.CharField(max_length=300)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('detail_item', kwargs = {
            'id': self.id,
        })

    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={
            'id': self.id,
        })

    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={
            'id': self.id,
        })


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.user}: order item is {self.item}'



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} order'

    def get_total_items(self):
        return f'{self.items.all()}'
    
    def get_total_items_sum(self):
        return sum([order_item.item.price*order_item.quantity for order_item in self.items.all()])