from django.contrib import admin
from .models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username', 'user__email')
    list_filter = ('user',)
    ordering = ('user',)
    fields = ('user', 'balance')
    readonly_fields = ('user',)

admin.site.register(Account, AccountAdmin)
