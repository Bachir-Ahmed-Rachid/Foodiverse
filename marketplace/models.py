from django.db import models

from accounts.models import User
from menu.models import Product

# Create your models here.
class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    fooditem=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    created_at=models.DateField(auto_now_add=True)
    modified_at=models.DateField(auto_now=True)

    def __unicode__(self):
        return self.user

