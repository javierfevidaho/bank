from django.contrib import admin
from .models import Account, Ticket, Cart, CartItem, WinningNumbers, Jackpot, Payment

class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username', 'user__email')
    list_filter = ('user',)
    ordering = ('user',)
    fields = ('user', 'balance')
    readonly_fields = ('user',)

class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'ticket_number', 'numbers', 'bonus', 'purchase_date', 'price', 'is_purchased', 'is_winner', 'win_amount', 'win_type', 'draw_date')
    search_fields = ('user__username', 'ticket_number', 'numbers')
    list_filter = ('user', 'purchase_date', 'is_purchased', 'is_winner', 'draw_date')
    ordering = ('purchase_date', 'user')
    fields = ('user', 'ticket_number', 'numbers', 'bonus', 'purchase_date', 'price', 'is_purchased', 'is_winner', 'win_amount', 'win_type', 'draw_date')
    readonly_fields = ('ticket_number', 'purchase_date')

class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)
    list_filter = ('user',)
    ordering = ('user',)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'ticket')
    search_fields = ('cart__user__username', 'ticket__ticket_number')
    list_filter = ('cart',)
    ordering = ('cart',)

class WinningNumbersAdmin(admin.ModelAdmin):
    list_display = ('draw_date', 'numbers', 'bonus', 'jackpot')
    search_fields = ('draw_date', 'numbers', 'bonus')
    list_filter = ('draw_date',)
    ordering = ('draw_date',)
    fields = ('draw_date', 'numbers', 'bonus', 'jackpot')

class JackpotAdmin(admin.ModelAdmin):
    list_display = ('amount', 'last_won')
    search_fields = ('amount', 'last_won')
    list_filter = ('last_won',)
    ordering = ('last_won',)
    fields = ('amount', 'last_won')
    readonly_fields = ('last_won',)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'stripe_charge_id', 'created_at', 'status')
    search_fields = ('user__username', 'stripe_charge_id')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
    fields = ('user', 'amount', 'stripe_charge_id', 'created_at', 'status')
    readonly_fields = ('user', 'amount', 'stripe_charge_id', 'created_at')

admin.site.register(Account, AccountAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(WinningNumbers, WinningNumbersAdmin)
admin.site.register(Jackpot, JackpotAdmin)
admin.site.register(Payment, PaymentAdmin)
