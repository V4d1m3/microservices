# Установка проекта

## Предварительные требования

- Python 3.8+
- Docker
- Docker Compose
- FastAPI

## Установка

    ```

1**Соберите и запустите сервисы:**

    Используйте Docker Compose для сборки и запуска всех сервисов, определенных в `compose.yml`.

    ```sh
    docker-compose up --build
    ```

2**Доступ к сервисам:**

    - `report_service`: http://localhost:8044/docs
    - `auth_service`: http://localhost:8001/docs
    - `announcement_service`: http://localhost:8033/docs
    - `db_service`: http://localhost:8090/docs


## Использование

- Логи сервисов можно найти в `*имя_сервиса*.log` файлах.
- Вы можете взаимодействовать с сервисами через их соответствующие конечные точки.

## Остановка сервисов

Для остановки сервисов выполните:

```sh
docker-compose down