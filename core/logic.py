from .models import Account, Transaction, Ticket

def deposit_money(user, amount):
    amount = float(amount)  # Convertir a float
    if amount > 0:
        account, created = Account.objects.get_or_create(user=user)
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='deposit', description='Deposit of BTC')

def buy_ticket(user, ticket_count):
    account = Account.objects.get(user=user)
    ticket_price = 10.00  # Supongamos que cada ticket cuesta 10
    total_cost = ticket_price * ticket_count
    if account.balance >= total_cost:
        account.balance -= total_cost
        account.save()
        for _ in range(ticket_count):
            Ticket.objects.create(user=user, price=ticket_price)
        Transaction.objects.create(account=account, amount=-total_cost, transaction_type='ticket_purchase', description=f'Purchase of {ticket_count} tickets')
    else:
        raise ValueError("Insufficient balance")
