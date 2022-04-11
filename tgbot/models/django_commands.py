import datetime

from birthdays.models import User, Birthday
from asgiref.sync import sync_to_async


@sync_to_async
def select_user(telegram_id: int):
    user = User.objects.filter(telegram_id=telegram_id).first()
    print(user.__str__())
    return user


@sync_to_async
def add_user(telegram_id, full_name, username):
    try:
        user = User(telegram_id=int(telegram_id), full_name=full_name, username=username).save()
        return user
    except Exception:
        user = User.objects.filter(telegram_id=telegram_id).first()
        print(user.__str__())
        return user


@sync_to_async
def count_user():
    return User.objects.all().count()


@sync_to_async
def add_birthday(telegram_id: int, name: str, birthday: datetime.date, phone_number: str = None):
    try:
        return Birthday(telegram_id=int(telegram_id), name=name, phone_number=phone_number, birthday=birthday).save()
    except Exception as e:
        print(e)

@sync_to_async
def select_all_birthdays(telegram_id: int):
    return Birthday.objects.filter(telegram_id=telegram_id).all()


@sync_to_async
def delete_all_birthdays(telegram_id: int):
    return Birthday.objects.filter(telegram_id=telegram_id).all().delete()
