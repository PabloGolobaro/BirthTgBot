from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template import loader

from birthdays.forms import BirthdayForm
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
    if request.method == 'POST':
        form = BirthdayForm(request.POST, instance=birthday)
        if form.is_valid():
            form.save()
            result = "Изменения успешно внесены"
        else:
            result = "Изменения не внесены"
        return render(request, 'birthdays/detail.html',
                      context={'form': form, "result": result, "birthday": birthday})

    else:
        form = BirthdayForm(instance=birthday)
        return render(request, 'birthdays/detail.html', {'form': form, "birthday": birthday})


# def index(request):
#     user_birthdays_list = Birthday.objects.all()
#     template = loader.get_template('birthdays/birthday.html')
#     context = {
#         'user_birthdays_list': user_birthdays_list,
#     }
#     # output = '----------- '.join([BD.__str__() for BD in user_birthdays_list])
#     return HttpResponse(template.render(context, request))
def add(request):
    if request.method == 'POST':
        form = BirthdayForm(request.POST)
        if form.is_valid():
            birthday = form.save(commit=False)
            birthday.user = request.user
            birthday.save()
            return HttpResponseRedirect('/done')
    else:
        form = BirthdayForm()
        return render(request, 'birthdays/add.html', context={'form': form})


def index(request):
    request: WSGIRequest
    if not request.user.is_anonymous:
        user_birthdays_list = Birthday.objects.filter(user=request.user)
        paginator = Paginator(user_birthdays_list, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj': page_obj,
        }
    else:
        context = {}
    return render(request, 'birthdays/index.html', context)


def done(request):
    return render(request, 'birthdays/done.html')
