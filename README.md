## Инструменты разработки
## Стек:
    Python >= 3.8
    Django==3.2.4
    Djangorestframework==3.12.4
    Djangorestframework-gis==0.17

# Старт
### 1) Клонировать репозиторий
    git clone ссылка_сгенерированная_в_вашем_репозитории
### 2) Создать образ
    docker-compose build
### 3) Запустить контейнер
    docker-compose up
### 4)Создать суперюзера
    Открыть вторую консоль и прописать следующие команды:
    1)docker exec -ti datum_geo_container bash
    2)python manage.py createsuperuser
### 5)Перейти по адресу
    http://127.0.0.1:8000/swagger/
### 6) Если нужно очистить БД
    docker-compose down -v
    