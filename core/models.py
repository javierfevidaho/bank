import uuid  # Asegúrate de importar el módulo uuid si lo vas a usar
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils import timezone

# Account model to track user's balance and details
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Balance: {self.balance}"

    def deposit(self, amount):
        self.balance += Decimal(amount)
        self.save()

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= Decimal(amount)
            self.save()
            return True
        return False

# Ticket model representing lottery tickets purchased by users
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    numbers = models.CharField(max_length=50)
    bonus = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('1.34'))
    is_purchased = models.BooleanField(default=False)
    draw_date = models.DateTimeField()
    purchase_date = models.DateTimeField()
    ticket_number = models.CharField(max_length=36, unique=True, blank=True, null=True)
    price_per_draw = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Campos adicionales
    is_winner = models.BooleanField(default=False)
    win_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    win_type = models.CharField(max_length=50, blank=True, null=True)
    next_drawing = models.DateTimeField()
    next_drawing = models.DateTimeField(null=True, blank=True)  # Asegúrate de agregar este campo
    

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = str(uuid.uuid4())
        super().save(*args, **kwargs)
    
# Model to store the winning numbers of each lottery draw
class WinningNumbers(models.Model):
    draw_date = models.DateField(unique=True)
    numbers = models.CharField(max_length=50)
    bonus = models.IntegerField()
    jackpot = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('5000.00'))

    def __str__(self):
        return f"Draw Date: {self.draw_date} - Numbers: {self.numbers} - Bonus: {self.bonus}"

# Cart model to hold tickets that the user wants to purchase
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart of {self.user.username}"

# CartItem model to hold individual tickets in a cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)

    def __str__(self):
        return f"CartItem - Cart: {self.cart.user.username} - Ticket: {self.ticket.id}"

# Payment model to track payments and their status
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    stripe_charge_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.user.username} - Amount: {self.amount} - Status: {self.status}"

# Jackpot model to represent jackpot amounts
class Jackpot(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    last_won = models.DateTimeField(null=False, blank=False, default=timezone.now)

    def __str__(self):
        return f"Jackpot of {self.amount} last won on {self.last_won}"
