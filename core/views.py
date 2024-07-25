import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from .models import Account, Ticket, Cart, CartItem, WinningNumbers, Jackpot
from decimal import Decimal
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from coinbase_commerce.client import Client
from datetime import datetime, timedelta
import random
from .models import WinningNumbers, Ticket
from django.shortcuts import render

stripe.api_key = settings.STRIPE_SECRET_KEY

def error_404(request, exception):
    return render(request, '404.html', status=404)

@login_required
def publish_winners(request):
    today = datetime.today()
    last_saturday = today - timedelta(days=today.weekday() + 2)
    winning_numbers, created = WinningNumbers.objects.get_or_create(draw_date=last_saturday)

    if created:
        winning_numbers.numbers = ','.join(map(str, random.sample(range(1, 36), 5)))
        winning_numbers.bonus = random.randint(1, 14)
        winning_numbers.jackpot = calculate_jackpot()
        winning_numbers.save()
        update_winners(winning_numbers)

    return render(request, 'core/winners.html', {'winning_numbers': winning_numbers})

def calculate_jackpot():
    last_winning = WinningNumbers.objects.order_by('-draw_date').first()
    if last_winning and not Ticket.objects.filter(is_winner=True, draw_date=last_winning.draw_date).exists():
        return last_winning.jackpot + 1000
    return 5000

def update_winners(winning_numbers):
    winning_tickets = Ticket.objects.filter(draw_date=winning_numbers.draw_date)
    for ticket in winning_tickets:
        user_numbers = set(map(int, ticket.numbers.split(',')))
        winning_set = set(map(int, winning_numbers.numbers.split(',')))
        match_count = len(user_numbers & winning_set)
        win_amount = 0
        win_type = "No Win"
        
        if match_count == 5 and ticket.bonus == winning_numbers.bonus:
            win_amount = winning_numbers.jackpot
            win_type = "Jackpot"
        elif match_count == 5:
            win_amount = 1000 * 1.34
            win_type = "5 Numbers"
        elif match_count == 4 and ticket.bonus == winning_numbers.bonus:
            win_amount = 300
            win_type = "4 + Bonus"
        elif match_count == 4:
            win_amount = 100 * 1.34
            win_type = "4 Numbers"
        elif match_count == 3 and ticket.bonus == winning_numbers.bonus:
            win_amount = 3 * 1.34
            win_type = "3 + Bonus"
        elif match_count == 3:
            win_amount = 1.34
            win_type = "3 Numbers"
        
        if win_amount > 0:
            ticket.is_winner = True
            ticket.win_amount = win_amount
            ticket.win_type = win_type
            ticket.save()
            account = Account.objects.get(user=ticket.user)
            account.balance += win_amount
            account.save()

@csrf_exempt
def guest_login(request):
    guest_user, created = User.objects.get_or_create(username='guest', defaults={'email': 'guest@example.com'})
    if created:
        guest_user.set_unusable_password()
        guest_user.save()
    login(request, guest_user)
    return JsonResponse({'success': True})

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

            # Asegúrate de convertir el monto a centavos correctamente
            amount = Decimal(data.get('amount', 0)) * 100  # Convertir a centavos

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Account Deposit',
                        },
                        'unit_amount': int(amount),  # Asegúrate de que amount sea un entero
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/cancel/'),
                client_reference_id=str(request.user.id)
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
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    if sig_header is None:
        return JsonResponse({'status': 'signature missing'}, status=400)

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
    if not request.user.is_authenticated or request.user.username == 'guest':
        return redirect('login')
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount'))
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
        except (InvalidOperation, ValueError):
            messages.error(request, 'Invalid amount entered.')
            return redirect('deposit')
        
        account, created = Account.objects.get_or_create(user=request.user)
        account.balance += amount
        account.save()
        messages.success(request, f'Successfully deposited ${amount}')
        return redirect('dashboard')
    return render(request, 'core/deposit.html')

@login_required
def winners(request):
    winning_tickets = Ticket.objects.filter(is_winner=True)
    return render(request, 'core/winners.html', {'winning_tickets': winning_tickets})

@login_required
def winning_numbers(request):
    winning_numbers = WinningNumbers.objects.all().order_by('-draw_date')
    return render(request, 'core/winning_numbers.html', {'winning_numbers': winning_numbers})

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
    if request.user.username == 'guest':
        return redirect('login')
    account, created = Account.objects.get_or_create(user=request.user)
    context = {
        'balance': account.balance if account else 0,
        'number_range': range(1, 36),
        'bonus_range': range(1, 15),
    }
    if request.method == 'POST':
        if 'bulk_tickets' in request.POST:
            bulk_tickets = json.loads(request.POST['bulk_tickets'])
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
                        price=Decimal('1.34')
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
                        price=Decimal('1.34')
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

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'cart_items_count': cart_items.count()})
    
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
            'amount': '1.34',
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
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Username', 'class': 'form-control'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password', 'class': 'form-control'}
        )
    )

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Username', 'class': 'form-control'}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password', 'class': 'form-control'}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}
        )
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
