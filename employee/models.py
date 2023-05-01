from django.contrib.auth import get_user_model
from django.db import models

from restaurant.models import Menu

User = get_user_model()


class Vote(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
