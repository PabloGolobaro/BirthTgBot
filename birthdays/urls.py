from django.urls import path

from . import views
app_name = 'birthdays'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:birthday_id>', views.detail, name='detail'),
    path('add', views.add, name='add'),
    path('done', views.done, name='done'),
]