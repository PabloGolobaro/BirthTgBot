from django.urls import path

from . import views
app_name = 'birthdays'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:birthday_id>/', views.detail, name='detail'),
    path('<int:birthday_id>/update/', views.update, name='update'),
]