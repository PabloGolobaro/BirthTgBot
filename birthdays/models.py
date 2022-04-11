from django.db import models


# Create your models here.
class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(TimeBasedModel):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    telegram_id = models.BigIntegerField(primary_key=True, verbose_name="ID telegram")
    full_name = models.CharField(max_length=100, verbose_name="Имя")
    username = models.CharField(max_length=100, verbose_name="Никнейм", null=True)

    def __str__(self):
        return f"{self.telegram_id}: {self.full_name} - {self.username}\n"


class Birthday(TimeBasedModel):
    class Meta:
        verbose_name = "День рождения"
        verbose_name_plural = "Дни рождения"

    id = models.AutoField(primary_key=True)
    telegram_id = models.BigIntegerField(verbose_name="ID telegram")
    # telegram_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ID telegram")
    name = models.CharField(max_length=100, verbose_name="ФИО")
    phone_number = models.CharField(max_length=100, verbose_name="Номер телефона", null=True)
    birthday = models.DateField(verbose_name="День рождения")

    def __str__(self):
        return f"Владелец {self.telegram_id}: {self.name} - {self.birthday}\n"
