from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Account, Ticket, WinningNumbers
from decimal import Decimal

@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

@receiver(post_save, sender=Ticket)
def update_account_balance(sender, instance, **kwargs):
    if instance.is_winner and instance.win_amount > 0:
        account, created = Account.objects.get_or_create(user=instance.user)
        account.balance += Decimal(instance.win_amount)
        account.save()

@receiver(post_save, sender=WinningNumbers)
def update_winning_tickets(sender, instance, created, **kwargs):
    if created:
        from .logic import update_winners
        update_winners(instance)
