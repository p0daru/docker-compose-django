from django.db import models
from djongo import models

class Customer(models.Model):
    name = models.CharField(max_length=100)  
    age = models.IntegerField() 
    gender = models.CharField(max_length=10) 
    email = models.EmailField(max_length=100)  

    def __str__(self):
        return self.name

class Ticket(models.Model):
    seat_number = models.IntegerField()  
    date = models.DateField() 
    time = models.TimeField()  
    movie_title = models.CharField(max_length=255)  

    def __str__(self):
        return f"{self.movie_title} ({self.date} - {self.time})"
    
class Seller(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    additional_info = models.TextField()

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)  
    seller = models.ForeignKey('djangoapp.Seller', on_delete=models.CASCADE)  
    order_date = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Order #{self.id} by {self.customer.name} for {self.ticket.movie_title}"
