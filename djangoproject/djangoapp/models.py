from django.db import models

# Модель для Глядачів
class Customer(models.Model):
    name = models.CharField(max_length=100)  # ПІБ
    age = models.IntegerField()  # Вік
    gender = models.CharField(max_length=10)  # Стать
    email = models.EmailField(max_length=100)  # Мейл для контакту

    def __str__(self):
        return self.name

# Модель для Квитків
class Ticket(models.Model):
    seat_number = models.IntegerField()  # Номер місця
    date = models.DateField()  # Дата сеансу
    time = models.TimeField()  # Час сеансу
    movie_title = models.CharField(max_length=255)  # Назва фільму

    def __str__(self):
        return f"{self.movie_title} ({self.date} - {self.time})"

# Модель для Продавців
class Seller(models.Model):
    name = models.CharField(max_length=100)  # ПІБ
    age = models.IntegerField()  # Вік
    gender = models.CharField(max_length=10)  # Стать
    additional_info = models.TextField(blank=True, null=True)  # Можливі інші дані

    def __str__(self):
        return self.name

# Модель для Замовлень (зв'язок між Глядачами і Квитками)
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Зв'язок з глядачем
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)  # Зв'язок з квитком
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)  # Зв'язок з продавцем
    order_date = models.DateTimeField(auto_now_add=True)  # Дата та час замовлення

    def __str__(self):
        return f"Order #{self.id} by {self.customer.name} for {self.ticket.movie_title}"
