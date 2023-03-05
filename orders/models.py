from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from accounts.models import Profile

from audioop import reverse
from django.utils.translation import gettext_lazy as _
from datetime import datetime

from creditcards.models import CardNumberField,CardExpiryField,SecurityCodeField

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_date= models.DateTimeField(verbose_name=_("Created At"), default=datetime.now)
    detils = models.ManyToManyField(Product , through='OrderDetails')
    is_finished = models.BooleanField()


    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return 'User: ' +  self.user.username + ', Order id: ' + str(self.id)

    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})


class OrderDetails(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    cost=models.DecimalField(max_digits=5,decimal_places=0,verbose_name=_("Cost"))
    quantity=models.IntegerField()
    class Meta:
        verbose_name = _("OrderDetails")
        verbose_name_plural = _("OrderDetailss")
    def __str__(self):
        return 'User: ' +  self.order.user.username + 'Product: '+ self.product.PRDname + 'Order id: ' + str(self.order.id)
    def get_absolute_url(self):
        return reverse("OrderDetails_detail", kwargs={"pk": self.pk})


class Checkout(models.Model):
    """Model definition for Checkout."""
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    country=models.CharField(max_length=100)
    adress=models.CharField(max_length=100)
    phone=models.CharField(max_length=20,verbose_name=_("phone"))
    cardholder=models.CharField(max_length=20,verbose_name=_("Card Holder"))
    cardnumber=CardNumberField(verbose_name=_("Card Number"),max_length=16)
    expire=CardExpiryField(verbose_name=_("Exepire Date"))
    security=SecurityCodeField(verbose_name=_("CCV"))
    order_delivery_date= models.DateTimeField(verbose_name=_("Delivery Date"),blank=True, null=True)

    def __str__(self):
        return 'User: ' +  self.order.user.username + ' --> Order id: ' + str(self.id)
    
    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        

