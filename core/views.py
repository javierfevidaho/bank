from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from .models import Account, Ticket, Cart, CartItem
from decimal import Decimal
from django.http import JsonResponse
from coinbase_commerce.client import Client
from django.conf import settings

@login_required
def dashboard(request):
    tickets = Ticket.objects.filter(user=request.user, is_purchased=True)
    return render(request, 'core/dashboard.html', {'tickets': tickets})

@login_required
def deposit(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        account, created = Account.objects.get_or_create(user=request.user)
        account.balance += Decimal(amount)
        account.save()
        messages.success(request, f'Successfully deposited ${amount}')
        return redirect('dashboard')
    return render(request, 'core/deposit.html')

@login_required
def profile(request):
    account, created = Account.objects.get_or_create(user=request.user)
    tickets = Ticket.objects.filter(user=request.user, is_purchased=True)
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('profile')
    return render(request, 'core/profile.html', {'account': account, 'tickets': tickets})

@login_required
def logout(request):
    auth_logout(request)
    return redirect('/accounts/login/')

@login_required
def purchase_ticket(request):
    account, created = Account.objects.get_or_create(user=request.user)
    context = {
        'balance': account.balance,
        'number_range': range(1, 36),
        'bonus_range': range(1, 15),
    }

    if request.method == 'POST':
        numbers = request.POST.getlist('numbers')
        bonus_number = request.POST.get('bonus')
        quantity = int(request.POST.get('quantity', 1))

        if len(numbers) != 5 or not bonus_number:
            messages.error(request, 'Please select 5 numbers and 1 bonus number.')
            return JsonResponse({'error': 'Please select 5 numbers and 1 bonus number.'}, status=400)

        try:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            for _ in range(quantity):
                ticket = Ticket(
                    user=request.user,
                    numbers=','.join(numbers),
                    bonus=int(bonus_number),
                    price=Decimal('1.00')
                )
                ticket.save()
                CartItem.objects.create(cart=cart, ticket=ticket)

            messages.success(request, f'{quantity} ticket(s) added to cart successfully.')
            return JsonResponse({'success': f'{quantity} ticket(s) added to cart successfully.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'core/purchase_ticket.html', context)

@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_cost = sum(item.ticket.price for item in cart_items)
    return render(request, 'core/cart.html', {'cart_items': cart_items, 'total_cost': total_cost})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('view_cart')

@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    account, created = Account.objects.get_or_create(user=request.user)
    total_cost = sum(item.ticket.price for item in cart_items)

    if account.balance >= total_cost:
        account.balance -= Decimal(total_cost)
        account.save()
        for item in cart_items:
            item.ticket.is_purchased = True
            item.ticket.save()
            item.delete()
        messages.success(request, f'Purchase successful. Total cost: ${total_cost}')
        return redirect('dashboard')
    else:
        messages.error(request, 'Insufficient balance')
        return render(request, 'core/cart.html', {'cart_items': cart_items, 'total_cost': total_cost, 'error': 'Insufficient balance'})

@login_required
def coinbase_payment(request):
    client = Client(api_key=settings.COINBASE_COMMERCE_API_KEY)
    domain_url = 'http://localhost:8000/'
    product = {
        'name': 'Lottery Ticket',
        'description': 'Purchase a lottery ticket',
        'local_price': {
            'amount': '1.00',
            'currency': 'USD'
        },
        'pricing_type': 'fixed_price',
        'redirect_url': domain_url + 'success/',
        'cancel_url': domain_url + 'cancel/',
    }
    charge = client.charge.create(**product)

    return render(request, 'core/coinbase_payment.html', {
        'charge': charge,
    })
