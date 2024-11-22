import time
from sqlalchemy import create_engine, Table, MetaData, select, func
from sqlalchemy.orm import sessionmaker

# Подключение к базе данных
DATABASE_URL = "sqlite:///./db.sqlite3"  # Пример для SQLite

# Создание подключения к базе данных
engine = create_engine(DATABASE_URL, echo=True)

# Создаем объект MetaData для работы с таблицами
metadata = MetaData()
metadata.bind = engine

# Подключаемся к базе данных и получаем таблицу 'issues'
issues = Table('technicalIssues_issues', metadata, autoload_with=engine)

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()


def timeOfPerfomance(query, description):
    # Замеряем время начала выполнения запроса
    start_time = time.time()

    # Выполним запрос
    result = session.execute(query).fetchall()

    # Замеряем время окончания выполнения
    end_time = time.time()

    execution_time = end_time - start_time  # Вычисляем время выполнения запроса

    # Выводим результат
    print(f"{description}: {execution_time:.20f}")

    # Печатаем данные
    for row in result:
        print(row)

    return 1


def timeOfFullBase():
    # Запрос для получения всех данных из таблицы
    query = select(issues)
    description = "execution_time_seconds(FullBase)"
    return timeOfPerfomance(query, description)


def timeOfFilterBase():
    # Запрос для фильтрации по полю 'controlCheck'
    query = select(issues).where(issues.c.controlCheck == True)
    description = "execution_time_seconds(FilterBase)"
    return timeOfPerfomance(query, description)


def timeOfAnnotateBase():
    # Запрос с аннотацией для вычисления длины поля 'concessionRequest'
    query = select(
        issues,
        func.length(issues.c.concessionRequest).label('concessionRequest_length')
    ).where(issues.c.controlCheck == True)
    description = "execution_time_seconds(AnnotateBase)"
    return timeOfPerfomance(query, description)


def timeOfValueBase():
    # Запрос для группировки по 'reporter_id' и подсчета количества записей
    query = select(
        issues.c.reporter_id,
        func.count(issues.c.id).label('request_count')
    ).group_by(issues.c.reporter_id)
    description = "execution_time_seconds(ValueBase)"
    return timeOfPerfomance(query, description)

start_time = time.time()
timeOfFullBase()
timeOfFilterBase()
timeOfAnnotateBase()
timeOfValueBase()
end_time = time.time()
print(end_time - start_time)
