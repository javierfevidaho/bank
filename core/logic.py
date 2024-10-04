import random
from decimal import Decimal
from .models import Ticket, WinningNumbers, Account

def calculate_jackpot():
    try:
        last_winning = WinningNumbers.objects.order_by('-draw_date').first()
        if last_winning and not Ticket.objects.filter(is_winner=True, draw_date=last_winning.draw_date).exists():
            return last_winning.jackpot + 1000
        return 5000
    except Exception as e:
        return 5000

def update_winners(winning_numbers):
    try:
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
                win_amount = 1000 * Decimal('1.34')
                win_type = "5 Numbers"
            elif match_count == 4 and ticket.bonus == winning_numbers.bonus:
                win_amount = 300
                win_type = "4 + Bonus"
            elif match_count == 4:
                win_amount = 100 * Decimal('1.34')
                win_type = "4 Numbers"
            elif match_count == 3 and ticket.bonus == winning_numbers.bonus:
                win_amount = 3 * Decimal('1.34')
                win_type = "3 + Bonus"
            elif match_count == 3:
                win_amount = Decimal('1.34')
                win_type = "3 Numbers"
            if win_amount > 0:
                ticket.is_winner = True
                ticket.win_amount = win_amount
                ticket.win_type = win_type
                ticket.save()
                account = Account.objects.get(user=ticket.user)
                account.balance += win_amount
                account.save()
    except Exception as e:
        print(f"Error updating winners: {e}")

def generate_winning_numbers():
    try:
        today = datetime.today()
        last_saturday = today - timedelta(days=today.weekday() + 2)
        winning_numbers, created = WinningNumbers.objects.get_or_create(draw_date=last_saturday)
        if created:
            winning_numbers.numbers = ','.join(map(str, random.sample(range(1, 36), 5)))
            winning_numbers.bonus = random.randint(1, 14)
            winning_numbers.jackpot = calculate_jackpot()
            winning_numbers.save()
            update_winners(winning_numbers)
        return winning_numbers
    except Exception as e:
        print(f"Error generating winning numbers: {e}")
        return None
