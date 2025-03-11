# Проект "Бюро находок"

## Запуск проекта

1. Создайте виртуальное окружение
2. Установите зависимости из файла requirements.txt
3. Создайте файл .env.local, используя .env.local.examples
4. Создайте DB, используя параметры из .env.local
5. Примените миграции
    ```bash
   alembic upgrade head 
    ```
6. Запустите сервер
   ```bash
   uvicorn main:app --reload
   ```

## Запуск автотестов

1. Создайте тестовую DB, используя параметры из .env.local
2. Запустите автотесты
   ```bash
   pytest -v
   ```
   
## Шпаргалка

### Alembic

1. Создание миграции
    ```bash
   alembic revision --autogenerate -m "comment"
    ```
2. Применение миграции
    ```bash
   alembic upgrade head 
    ```
3. Откатить последнюю миграцию
   ```bash
   alembic downgrade head-1
   ```
4. 
   