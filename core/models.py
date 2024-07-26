from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from decimal import Decimal

class WinningNumbers(models.Model):
    draw_date = models.DateField(unique=True)
    numbers = models.CharField(max_length=20)
    bonus = models.IntegerField()
    jackpot = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00)

    def __str__(self):
        return f"Winning Numbers for {self.draw_date}"

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=10, unique=True, blank=True)
    numbers = models.CharField(max_length=20)
    bonus = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    draw_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=1.34)
    is_purchased = models.BooleanField(default=False)
    is_winner = models.BooleanField(default=False)
    win_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    win_type = models.CharField(max_length=20, default="No Win")

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

class Jackpot(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00)
    last_won = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Jackpot of {self.amount}"
