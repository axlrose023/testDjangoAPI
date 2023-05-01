from django.urls import path
from employee.views import (EmployeeView, LoginView, index, vote, votes, MenuView)

urlpatterns = [
    path('create/', EmployeeView.as_view(), name='employee_creation'),
    path('login/', LoginView.as_view(), name='employee_login'),
    path('', index, name='index'),
    path('vote/<int:id>/', vote, name='vote'),
    path('votes/', votes, name='votes'),
    path('current_menus/', MenuView.as_view()),
]
