from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=10, unique=True, blank=True)
    numbers = models.CharField(max_length=20)
    bonus = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=1.00)
    is_purchased = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'numbers', 'bonus')

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = self.generate_unique_ticket_number()
        super().save(*args, **kwargs)

    def generate_unique_ticket_number(self):
        while True:
            ticket_number = get_random_string(10)
            if not Ticket.objects.filter(ticket_number=ticket_number).exists():
                return ticket_number

    def __str__(self):
        return f"Ticket {self.ticket_number} for {self.user.username}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    def __str__(self):
        return f"CartItem {self.ticket.ticket_number} in cart of {self.cart.user.username}"

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Account of {self.user.username}"
