from django.contrib import admin
from .models import Client, Link

# Register your models here.


class ClientAdmin(admin.ModelAdmin):
    list_display = ("client_name", "is_premium_client",)


class LinkAdmin(admin.ModelAdmin):
    list_display = ("original_link", "shortened_link",
                    "creation_date", "access_counter", "client",)


admin.site.register(Client, ClientAdmin)
admin.site.register(Link, LinkAdmin)
