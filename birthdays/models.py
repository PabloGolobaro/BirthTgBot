from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# class Telegram_user(TimeBasedModel, User):
#     class Meta:
#         verbose_name = "Пользователь"
#         verbose_name_plural = "Пользователи"
#
#     telegram_id = models.BigIntegerField(primary_key=True, verbose_name="ID telegram")
#     full_name = models.CharField(max_length=100, verbose_name="Имя")
#
#     # username = models.CharField(max_length=100, verbose_name="Никнейм", null=True)
#
#     def __str__(self):
#         return f"{self.telegram_id}: {self.full_name} - {self.username}\n"


class Birthday(TimeBasedModel):
    class Meta:
        verbose_name = "День рождения"
        verbose_name_plural = "Дни рождения"

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name="ФИО")
    phone_number = models.CharField(max_length=100, verbose_name="Номер телефона", null=True)
    birthday = models.DateField(verbose_name="День рождения")

    def __str__(self):
        return f"Пользователь {self.user.username}- {self.user.telegram_id}:{self.name} - {self.birthday}\n"
