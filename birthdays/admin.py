from django.contrib import admin
from birthdays.models import Birthday


# Register your models here.
@admin.register(Birthday)
class UserAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "phone_number", "birthday")
