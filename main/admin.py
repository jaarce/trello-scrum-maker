from django.contrib import admin
from main.models import *


class AccountsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Accounts, AccountsAdmin)