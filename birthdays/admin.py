from django.contrib import admin
from birthdays.models import User, Birthday


# Register your models here.
@admin.register(Birthday)
class UserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "name", "phone_number", "birthday")


admin.site.register(User)
