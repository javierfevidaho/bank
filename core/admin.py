# admin.py
from django.contrib import admin
from .models import Account, Ticket, Cart, CartItem

class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username', 'user__email')
    list_filter = ('user',)
    ordering = ('user',)
    fields = ('user', 'balance')
    readonly_fields = ('user',)

class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'ticket_number', 'numbers', 'bonus', 'purchase_date', 'price', 'is_purchased')
    search_fields = ('user__username', 'ticket_number', 'numbers')
    list_filter = ('user', 'purchase_date', 'is_purchased')
    ordering = ('purchase_date', 'user')
    fields = ('user', 'ticket_number', 'numbers', 'bonus', 'purchase_date', 'price', 'is_purchased')
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

admin.site.register(Account, AccountAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
