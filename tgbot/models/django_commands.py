import datetime

from birthdays.models import Birthday
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User


@sync_to_async
def select_user(telegram_id):
    user = User.objects.get(telegram_id=telegram_id)
    print(user.__str__())
    return user


@sync_to_async
def add_user(password, telegram_id, full_name, username):
    try:
        user = User(telegram_id=int(telegram_id), full_name=full_name, username=username)
        user.set_password(password)
        user.save()
        print(f"User added {user}")
        return user
    except:
        user = User.objects.get(telegram_id=telegram_id)
        print(f"User is already exists {user}")
        return user


@sync_to_async
def count_user():
    return User.objects.all().count()


@sync_to_async
def add_birthday(telegram_id: int, name: str, birthday: datetime.date, phone_number: str = None):
    try:
        user = User.objects.get(telegram_id=telegram_id)
        return Birthday(user=user, name=name, phone_number=phone_number, birthday=birthday).save()
    except Exception as e:
        print(e)


@sync_to_async
def select_all_birthdays(telegram_id: int):
    return Birthday.objects.filter(user__telegram_id=telegram_id).all()


@sync_to_async
def delete_all_birthdays(telegram_id: int):
    return Birthday.objects.filter(user__telegram_id=telegram_id).all().delete()
