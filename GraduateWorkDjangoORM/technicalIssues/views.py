from django.db.models import Count
from django.db.models.functions import Length
from django.shortcuts import render, redirect, get_object_or_404
from technicalIssues.forms import ClassOfEngineer, SignUpForm, AddIssue, AddReport
from technicalIssues.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
import time
from django.http import JsonResponse

# from technicalIssues.forms import SignUpForm

main_issue = 1  # ID запроса, который выбирается как особоважный и выводится на главной странице


# Create your views here.


def cons_request(request):
    '''
    Функция которая передает в html шаблон все запросы из базы данных.
    А так же отслеживает нажате на кнопку, которая привязана к номеру запроса и сохраняет в main_issue
    ID запроса, для отображения на главной странице
    '''
    title = 'Запросы от производства'
    global main_issue
    issues_table = Issues.objects.all()
    context = {
        'title': title,
        'issues_table': issues_table,
        # 'main_issue': main_issue
    }
    if request.method == 'POST':
        product_id = request.POST.get('main_issue')
        if product_id:
            product_id = int(product_id)
            main_issue = Issues.objects.get(id=product_id).id
            print(main_issue)

    return render(request, 'request.html', context)


def main_page(request):
    '''
    Функция которая передает в html шаблон запрос который соответствует id=main_issue
    '''
    title = 'Запросы от производства'
    global main_issue
    issues_table = Issues.objects.filter(id=main_issue)
    context = {
        'title': title,
        'main_issue': main_issue,
        'issues_table': issues_table
    }
    return render(request, 'main.html', context)


def filter_check(request):  #  Проверенные запросы
    '''
    Функция которая передает в html шаблон запрос который соответствует controlCheck=True, проверенные запросы
    '''
    title = 'Проверенные запросы'
    issues_table = Issues.objects.filter(controlCheck=True)
    context = {
        'title': title,
        'issues_table': issues_table
    }
    return render(request, 'request.html', context)


def filter_report(request):  #  Запросы ожидающие решения
    '''
    Функция которая передает в html шаблон запрос который соответствует concessionReport='', запросы без решения
    '''
    title = 'Запросы ожидающие решения'
    issues_table = Issues.objects.filter(concessionReport='')
    context = {
        'title': title,
        'issues_table': issues_table
    }
    return render(request, 'request.html', context)


def signup(request):
    '''
    Функция взаимодействет с POST запросом для получения данных регистрации пользователя и проведения валидации данных.
    Данные пользователя передаются в функцию login библиотеки django.contrib.auth для внесеня данных и авторизации
    '''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически авторизует пользователя после регистрации
            return redirect('login')  # Перенаправляем на страницу входа (или на любую другую страницу)
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def add_issue_view(request):  #  Внесение данных в таблицу
    '''
    Функция по созданию нового запроса.
    Функция написана с учетом декоратора @login_required. Доступ ограничен для незарегистрированных пользователей
    Функция взаимодействет с POST запросом для переноса данных из формы в базу данных.
    '''

    if request.method == 'POST':
        form = AddIssue(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = request.user
            issue.save()
            return redirect('main_page')  # Перенаправление после успешного сохранения
    else:
        form = AddIssue()

    return render(request, 'add_request.html', {'form': form})


@login_required
def add_report_view(request, request_nb):  #  Внесение данных в таблицу
    '''
    Функция по корректировке запроса по ID номеру - request_nb.
    Функция написана с учетом декоратора @login_required. Доступ ограничен для незарегистрированных пользователей
    Функция взаимодействет с POST запросом для переноса данных из формы в базу данных.
    : param request_nb: int
    '''
    issue = get_object_or_404(Issues, id=request_nb)  # Получаем конкретную запись
    if request.method == 'POST':
        form = AddReport(request.POST, instance=issue)  # Передаём существующий объект в форму
        if form.is_valid():
            updated_issue = form.save(commit=False)
            updated_issue.reporter = request.user  # Обновляем поле "reporter"
            updated_issue.save()  # Сохраняем изменения в базе данных
            return redirect('main_page')  # Перенаправление после успешного сохранения
    else:
        form = AddReport(instance=issue)  # Инициализируем форму с данными существующей записи

    context = {
        'form': form,
        'issue': issue
    }

    return render(request, 'add_report.html', context)


def custom_logout_view(request):  # Функция описывающая выход из системы
    '''
    Функция описывающая выход из системы
    '''
    logout(request)
    return redirect('/')


def timeOfPerfomance(base, description):
    start_time = time.time()  # Замеряем время начала выполнения
    # this_base = base
    data = list(base)
    end_time = time.time()  # Замеряем время конца выполнения

    execution_time = end_time - start_time  # Вычисляем время выполнения запроса

    data.append({description: execution_time})  # Добавляем время выполнения в результат JSON
    print(f"{description}: {execution_time:.20f}")
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

def timeOfFullBase(request):

    fullBase = Issues.objects.all().values()
    description = "execution_time_seconds(FullBase)"
    return timeOfPerfomance(fullBase, description)

def timeOfFilterBase(request):
    filterBase = Issues.objects.filter(controlCheck=True).values()
    description = "execution_time_seconds(FilterBase)"
    return timeOfPerfomance(filterBase, description)

def timeOfAnnotateBase(request):
    filterBase = Issues.objects.filter(controlCheck=True) \
        .annotate(concessionRequest_length=Length('concessionRequest')) \
        .values()
    description = "execution_time_seconds(AnnotateBase)"
    return timeOfPerfomance(filterBase, description)

def timeOfValueBase(request):
    # filterBase = Issues.objects.values('reporter').annotate(request_count=Count('id'))
    filterBase = Issues.objects.values('reporter_id') \
                                 .annotate(request_count=Count('id'))

    description = "execution_time_seconds(ValueBase)"
    return timeOfPerfomance(filterBase, description)


# Резервная информация на дальнейше внедрение
# from django.db.models import Count, Sum, Avg
#
# # Пример: количество запросов по каждому пользователю
# user_issue_count = Issues.objects.values('user').annotate(count=Count('id'))
#
# # Пример: среднее значение по какому-то полю
# average_report_count = Issues.objects.aggregate(Avg('reportCount'))
