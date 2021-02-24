from django.db import models
from django.contrib.auth.models import User
# Create your models here.
STATE_CHOICE =(
    ('Utterpradesh','Utterpradesh'),
    ('Mumbai','Mumbai'),
    ('delhi','delhi'),
    ('Kolkata','Kolkata'),
    ('Punjab','Punjab'),
    ('Gujrat','Gujrat'),
)
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name =models.CharField(max_length=50)
    locality = models.CharField( max_length=50)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICE,max_length=50)
CATEGOTY_CHOICES= (
    ('m','mobile'),
    ('tw','topwear'),
    ('bw','bottomwear'),
)
class Product(models.Model):
    title = models.CharField( max_length=50)
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    discription = models.TextField()
    brand = models.CharField( max_length=50)
    category = models.CharField(choices=CATEGOTY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='productimg')
STATES_CHOICES=(
    ('Accepted','Accepted'),
    ('packed','packed'),
    ('On the Way','On the Way'),
    ('Cancel','Cancel'),
)
class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    orderplaced_time =models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATES_CHOICES, max_length=50,default='pending')
    @property
    def total_cost(self):
        return self.quantity*self.product.discount_price


class Cart(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    product =models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity*self.product.discount_price
