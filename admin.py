from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Shopify

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ShopifyInline(admin.StackedInline):
    model = Shopify
    can_delete = False
    verbose_name_plural = 'Shopify'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ShopifyInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)