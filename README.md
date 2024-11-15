**Приложение для сбора и отработки конструктивных замечаний**

Это веб-приложение, предназначенное для сбора и обработки конструктивных замечаний. Оно предоставляет пользователям возможность вносить и получать данные через удобный веб-интерфейс. Доступ к внесению данных ограничен только зарегистрированными пользователями, что обеспечивает безопасность и контроль над базой данных. Также предусмотрены функции фильтрации и параллельной работы с базой данных.

**Описание функциональности**

*   Внесение данных: Только зарегистрированные пользователи могут добавлять конструктивные замечания.
*   Фильтрация запросов: Пользователи могут фильтровать замечания по различным критериям.
*   Параллельная работа с базой данных: Приложение позволяет нескольким пользователям работать с данными одновременно, минимизируя риск конфликтов.
*   Безопасность: Приложение ограничивает несанкционированное влияние на базу данных, защищая данные от случайных или злонамеренных изменений.

**Технологии**

    Django: Фреймворк для разработки веб-приложений на Python.
    asgiref: Асинхронный сервер для работы с Django.
    sqlparse: Библиотека для парсинга SQL-запросов.
    typing_extensions: Поддержка аннотаций типов в Python.
    tzdata: Данные о временных зонах для работы с датами и временем.

**Установка и запуск**

    Клонируйте репозиторий:

git clone https://github.com/Coldrik/GraduateWork.git

Перейдите в директорию проекта:

cd GraduateWork

Установите зависимости:

pip install -r requirements.txt

Настройте базу данных и примените миграции:

python manage.py migrate

Создайте суперпользователя для администрирования:

python manage.py createsuperuser

Запустите сервер разработки:

    python manage.py runserver

    Перейдите в браузер и откройте http://127.0.0.1:8000, чтобы начать использовать приложение.
