import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from .models import Account, Ticket, Cart, CartItem
from decimal import Decimal
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return JsonResponse({'refresh': str(refresh), 'access': str(refresh.access_token)})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

@login_required
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST

            amount = int(data.get('amount', 0)) * 100  # Convert to cents

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Account Deposit',
                        },
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/cancel/'),
                client_reference_id=str(request.user.id)  # Añadir la referencia del cliente
            )
            return HttpResponseRedirect(checkout_session.url)
        except Exception as e:
            return JsonResponse({'error': str(e)})

@login_required
def dashboard(request):
    tickets = Ticket.objects.filter(user=request.user, is_purchased=True)
    account, created = Account.objects.get_or_create(user=request.user)
    return render(request, 'core/dashboard.html', {'tickets': tickets, 'account': account})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return JsonResponse({'status': 'invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'status': 'invalid signature'}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_session(session)
    return JsonResponse({'status': 'success'})

def handle_checkout_session(session):
    user_id = session.get('client_reference_id')
    if user_id:
        user = get_object_or_404(User, id=int(user_id))
        amount = Decimal(session['amount_total']) / 100
        account, created = Account.objects.get_or_create(user=user)
        account.balance += amount
        account.save()

@login_required
def success(request):
    return render(request, 'core/success.html')

@login_required
def cancel(request):
    return render(request, 'core/cancel.html')

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
        if 'bulk_tickets' in request.body:
            data = json.loads(request.body)
            bulk_tickets = data.get('bulk_tickets', [])
            try:
                cart, _ = Cart.objects.get_or_create(user=request.user)
                tickets = []
                for ticket in bulk_tickets:
                    ticket_numbers = ','.join(map(str, ticket['numbers']))
                    ticket_bonus = int(ticket['bonus'])
                    new_ticket = Ticket(
                        user=request.user,
                        numbers=ticket_numbers,
                        bonus=ticket_bonus,
                        price=Decimal('1.00')
                    )
                    new_ticket.save()
                    tickets.append(new_ticket)
                    CartItem.objects.create(cart=cart, ticket=new_ticket)
                messages.success(request, f'{len(tickets)} ticket(s) added to cart successfully.')
                return JsonResponse({'success': f'{len(tickets)} ticket(s) added to cart successfully.', 'tickets': [t.id for t in tickets]})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            numbers = request.POST.getlist('numbers')
            bonus_number = request.POST.get('bonus')
            quantity = int(request.POST.get('quantity', 1))
            if len(numbers) != 5 or not bonus_number:
                messages.error(request, 'Please select 5 numbers and 1 bonus number.')
                return JsonResponse({'error': 'Please select 5 numbers and 1 bonus number.'}, status=400)

            if Ticket.objects.filter(user=request.user, numbers=','.join(numbers), bonus=int(bonus_number)).exists():
                return JsonResponse({'error': 'Duplicate ticket not allowed.'}, status=400)

            try:
                cart, _ = Cart.objects.get_or_create(user=request.user)
                tickets = []
                for _ in range(quantity):
                    ticket = Ticket(
                        user=request.user,
                        numbers=','.join(numbers),
                        bonus=int(bonus_number),
                        price=Decimal('1.00')
                    )
                    ticket.save()
                    tickets.append(ticket)
                    CartItem.objects.create(cart=cart, ticket=ticket)
                messages.success(request, f'{quantity} ticket(s) added to cart successfully.')
                return JsonResponse({'success': f'{quantity} ticket(s) added to cart successfully.', 'tickets': [t.id for t in tickets]})
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
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart_item.delete()
        messages.success(request, 'Item removed from cart.')
    except CartItem.DoesNotExist:
        messages.error(request, 'Item not found or does not belong to you.')
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
    return render(request, 'core/coinbase_payment.html', {'charge': charge})

@login_required
def payment(request):
    return render(request, 'core/payment.html', {'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def purchase_ticket(request):
    account, created = Account.objects.get_or_create(user=request.user)
    context = {
        'balance': account.balance,
        'number_range': range(1, 36),
        'bonus_range': range(1, 15),
    }

    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            tickets = data.get('tickets', [])
            if not tickets:
                return JsonResponse({'error': 'No tickets provided'}, status=400)
            
            try:
                cart, _ = Cart.objects.get_or_create(user=request.user)
                for ticket_data in tickets:
                    numbers = ticket_data['numbers']
                    bonus_number = ticket_data['bonus']
                    if Ticket.objects.filter(user=request.user, numbers=','.join(map(str, numbers)), bonus=int(bonus_number)).exists():
                        continue  # Skip duplicates

                    ticket = Ticket(
                        user=request.user,
                        numbers=','.join(map(str, numbers)),
                        bonus=int(bonus_number),
                        price=Decimal('1.00')
                    )
                    ticket.save()
                    CartItem.objects.create(cart=cart, ticket=ticket)
                return JsonResponse({'success': 'Tickets added to cart successfully.'})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            numbers = request.POST.getlist('numbers')
            bonus_number = request.POST.get('bonus')
            if len(numbers) != 5 or not bonus_number:
                return JsonResponse({'error': 'Please select 5 numbers and 1 bonus number.'}, status=400)

            if Ticket.objects.filter(user=request.user, numbers=','.join(numbers), bonus=int(bonus_number)).exists():
                return JsonResponse({'error': 'Duplicate ticket not allowed.'}, status=400)

            try:
                cart, _ = Cart.objects.get_or_create(user=request.user)
                ticket = Ticket(
                    user=request.user,
                    numbers=','.join(numbers),
                    bonus=int(bonus_number),
                    price=Decimal('1.00')
                )
                ticket.save()
                CartItem.objects.create(cart=cart, ticket=ticket)
                return JsonResponse({'success': 'Ticket added to cart successfully.', 'ticket_id': ticket.id})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
    return render(request, 'core/purchase_ticket.html', context)
