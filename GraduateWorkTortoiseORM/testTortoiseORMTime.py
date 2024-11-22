import time
from tortoise import Tortoise, fields
from tortoise.models import Model
from tortoise.functions import Length, Count
import asyncio

# Подключение к базе данных
DATABASE_URL = "sqlite://db.sqlite3"

# Модель для таблицы
class TechnicalIssue(Model):
    id = fields.IntField(pk=True)
    dwg = fields.CharField(max_length=200)
    concessionRequest = fields.TextField()
    controlCheck = fields.BooleanField()
    caseOfProblem = fields.TextField()
    concessionReport = fields.TextField()
    reporter_id = fields.IntField()
    user_id = fields.IntField()

    class Meta:
        table = "technicalIssues_issues"

# Инициализация подключения к базе данных
async def init_db():
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={'models': ['__main__']}
    )
    await Tortoise.generate_schemas()

# Замер времени выполнения запроса
async def time_of_performance(query, description: str):
    start_time = time.time()

    # Выполняем запрос
    result = await query

    # Замеряем время окончания выполнения
    end_time = time.time()

    execution_time = end_time - start_time  # Вычисляем время выполнения запроса
    print(f"{description}: {execution_time:.20f}")

    # Для проверки вывода результатов расскоментировать
    # for row in result:
    #     print(row)

    return result

# Запрос для получения всех данных из таблицы
async def time_of_full_base():
    query = TechnicalIssue.all()  # Получаем все записи
    description = "execution_time_seconds(FullBase)"
    result = query.values()
    return await time_of_performance(result, description)

# Запрос для фильтрации по полю 'controlCheck'
async def time_of_filter_base():
    query = TechnicalIssue.filter(controlCheck=True)  # Фильтруем по controlCheck
    description = "execution_time_seconds(FilterBase)"
    result = query.values()
    return await time_of_performance(result, description)

# Запрос с аннотацией для вычисления длины поля 'concessionRequest'
async def time_of_annotate_base():
    query = TechnicalIssue.filter(controlCheck=True).annotate(
        concessionRequest_length=Length('concessionRequest')  # Используем Length для вычисления длины
    )  # Добавляем длину поля 'concessionRequest'
    result = query.values()
    description = "execution_time_seconds(AnnotateBase)"
    return await time_of_performance(result, description)


# Запрос для группировки по 'reporter_id' и подсчета количества записей
async def time_of_value_base():
    query = TechnicalIssue.annotate(
        request_count=Count('id')  # Подсчитываем количество записей по reporter_id
    ).group_by('reporter_id')  # Группируем по reporter_id

    # используем values() для получения данных
    result = query.values('reporter_id', 'request_count')

    description = "execution_time_seconds(ValueBase)"
    return await time_of_performance(result, description)




# Основная асинхронная функция для выполнения всех запросов
async def main():
    await init_db()  # Инициализируем подключение и создаём схемы

    # Используем asyncio.gather для параллельного выполнения запросов
    # await asyncio.gather(
    #     time_of_full_base(),
    #     time_of_filter_base(),
    #     time_of_annotate_base(),
    #     time_of_value_base()
    # )

    # Запускаем все запросы
    start_time = time.time()
    await time_of_full_base()
    await time_of_filter_base()
    await time_of_annotate_base()
    await time_of_value_base()
    end_time = time.time()

    print(f"Total execution time: {end_time - start_time:.20f} seconds")

# Запуск программы
if __name__ == "__main__":
    asyncio.run(main())
