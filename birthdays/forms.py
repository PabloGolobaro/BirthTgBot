from django import forms
from .models import Birthday


# class FeedbackForm(forms.Form):
#     name = forms.CharField(label='Имя', max_length=20, min_length=2, error_messages={
#         'max_length': 'Слишком много символов',
#         'min_length': 'Слишком мало символов',
#         'required': 'Укажите хотя бы один символ',
#     })
#     surname = forms.CharField()
#     feedback = forms.CharField(widget=forms.Textarea(attrs={"cols": "20", "rows": "5"}))
#     rating = forms.IntegerField(label='Рейтинг', max_value=5, min_value=1)

class BirthdayForm(forms.ModelForm):
    class Meta:
        model = Birthday
        # fields = ['name', 'surname', 'rating', 'feedback']
        exclude = ["user"]
        fields = '__all__'
        labels = {
            'name': 'ФИО',
            'phone_number': 'Номер телефона',
            'birthday': 'День рождения',
        }
        error_messages = {
            'name': {
                'max_length': 'Слишком много символов',
                'min_length': 'Слишком мало символов',
                'required': 'Укажите хотя бы один символ',
            },
            'surname': {
                'max_length': 'Слишком много символов',
                'min_length': 'Слишком мало символов',
                'required': 'Укажите хотя бы один символ',
            },

        }
