"""
URL configuration for GraduateWorkDjangoORM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from technicalIssues.views import (cons_request, main_page, filter_check, signup, filter_report, add_issue_view,
                                   custom_logout_view, add_report_view, timeOfFullBase, timeOfFilterBase,
                                   timeOfAnnotateBase, timeOfValueBase)
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),  #  админская панель
    path('', main_page, name='main_page'),  #  главная страница
    # path('reg/', class_of_engineer_view),
    path('request/', cons_request),  # Страница с отображением всех запросов
    path('filter/check', filter_check),  # Страница с отображением проверенных запросов
    path('login/', auth_views.LoginView.as_view(), name='login'),  #  Страница авторизации
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('signup/', signup, name='signup'), #  страница регистрации пользователя
    path('logout/', custom_logout_view, name='logout'),  # Выход из системы
    path('filter/report', filter_report), #  Страница с отображением запросов без решений
    path('add_request', add_issue_view),  # Страница добавления запроса
    path('add_report/<int:request_nb>', add_report_view),  # Страница добавления решения к конкретному запросу
    path('timeOfFullBase/', timeOfFullBase, name='timeOfFullBase'),
    path('timeOfFilterBase/', timeOfFilterBase, name='timeOfFilterBase'),
    path('timeOfAnnotateBase/', timeOfAnnotateBase, name='timeOfAnnotateBase'),
    path('timeOfValueBase/', timeOfValueBase, name='timeOfValueBase'),

]
