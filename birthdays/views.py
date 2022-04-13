from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template import loader

from birthdays.models import Birthday
from django.shortcuts import render


# def detail(request, birthday_id):
#     try:
#         birthday = Birthday.objects.get(pk=birthday_id)
#     except Birthday.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'birthdays/datail.html', {'birthday': birthday})
def detail(request, birthday_id):
    birthday = get_object_or_404(Birthday, pk=birthday_id)
    return render(request, 'birthdays/detail.html', {'birthday': birthday})

# def index(request):
#     user_birthdays_list = Birthday.objects.all()
#     template = loader.get_template('birthdays/birthday.html')
#     context = {
#         'user_birthdays_list': user_birthdays_list,
#     }
#     # output = '----------- '.join([BD.__str__() for BD in user_birthdays_list])
#     return HttpResponse(template.render(context, request))
def update(request, birthday_id):
    return HttpResponse("You're updating on birthday %s." % birthday_id)
def index(request):
    user_birthdays_list = Birthday.objects.all()
    context = {
        'user_birthdays_list': user_birthdays_list,
    }
    return render(request, 'birthdays/birthday.html', context)
