## Django Polls API

Тестовое задание для Фабрики Решений.

## Функционал
* авторизация в системе;
* добавление/изменение/удаление опросов (суперпользователь);
* добавление/изменение/удаление вопросов в опросе (суперпользователь);
* получение списка активных опросов;
* прохождение опроса (в том числе анонимно);
* получение пройденных пользователем опросов с детализацией по ответам по уникальному ID пользователя.
## Запуск
* ####  Склонировать этот репозиторий
* ####  В корне проекта поднять Docker
        docker-compose up --build
* #### Для просмотра документации перейти по адресу
        http://127.0.0.1:8000/api/v1/swagger/
* #### При первом запуске создается суперпользователь (su:101010)
* #### При первом запуске генерируются некоторые данные в БД (опросы, вопросы, варианты ответа)

