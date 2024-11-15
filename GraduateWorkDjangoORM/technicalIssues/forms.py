from django import forms
from django.core.validators import RegexValidator
from technicalIssues.models import Issues
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# class UserRegister (forms.Form):
#     username = forms.CharField(max_length=30, label='Введите логин:')
#     password = forms.CharField(max_length=8, label='Введите пароль:')
#     repeat_password = forms.CharField(max_length=8, label='Повторите пароль:')
#
#     age = forms.CharField(max_length=3,
#                           validators=[RegexValidator(regex=r'^\d+$',  # только цифры
#                                                      message='Введите только цифры.',
#                                                      code='invalid')],
#                           label='Введите свой возраст:',
#                           widget=forms.NumberInput())


class ClassOfEngineer(forms.ModelForm):

    username = forms.CharField(max_length=30, label='Введите логин:')
    password = forms.CharField(max_length=8, label='Введите пароль:')
    repeat_password = forms.CharField(max_length=8, label='Повторите пароль:')

    age = forms.CharField(max_length=3,
                          validators=[RegexValidator(regex=r'^\d+$',  # только цифры
                                                     message='Введите только цифры.',
                                                     code='invalid')],
                          label='Введите свой возраст:',
                          widget=forms.NumberInput())


class SignUpForm(UserCreationForm):
    # email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']  # ['username', 'email', 'password1', 'password2']


class AddIssue (forms.ModelForm):
    class Meta:
        model = Issues
        fields = ['dwg', 'concessionRequest', 'caseOfProblem']
        labels = {'dwg': 'Конструктивная группа',
                  'concessionRequest': 'Введите текст запроса',
                  'caseOfProblem': 'Введите описание причины'}

class AddReport (forms.ModelForm):
    class Meta:
        model = Issues
        fields = ['controlCheck', 'concessionReport']
        labels = {'controlCheck': 'Отметка о проверке запроса',
                  'concessionReport': 'Введите описание решения'}

