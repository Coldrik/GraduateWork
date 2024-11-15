from django.db import models
from django import forms
from django.contrib.auth.models import User


# Create your models here.
# class Engineer(models.Model):
#     processEngineer = 'PE'
#     controlEngineer = 'CE'
#     designEngineer = 'DE'
#
#     STATUS_CHOICES = [
#         (processEngineer, 'Process Engineer'),
#         (controlEngineer, 'Control Engineer'),
#         (designEngineer, 'Design Engineer'),
#     ]
#
#     status = models.CharField(
#         max_length=2,
#         choices=STATUS_CHOICES,
#         default=processEngineer,
#     )
#     name = models.CharField(max_length=200)  # имя покупателя(username аккаунта)
#     age = models.IntegerField(default=0)  # возраст
#
#     def __str__(self):
#         return self.name


class Issues(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1,
        related_name='created_issues')  # Пользователь, который создает запрос
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, default=1,
        related_name='reported_issues')  # Пользователь, который выдает решение
    dwg = models.CharField(max_length=200)  # обозначение конструктивной группы
    concessionRequest = models.TextField()  # Описание отклонения, запрос
    controlCheck = models.BooleanField(default=False)
    caseOfProblem = models.TextField()  # Причина проблемы
    concessionReport = models.TextField()  # описание решения
    # productionList = models.TextField()  # описание решения

    # engineer = models.ManyToManyField(Engineer, related_name='Issues')

    def __str__(self):
        return self.dwg


