# Devman Tg Bot Starter Pack

Шаблон веб-приложения Django с чат-ботом Telegram. Подходит для быстрого запуска разработки нового ПО. Позволяет всего за час подготовить свою первую сборку ПО и запустить её на сервере.

Второе предназначение Starter Pack — это быть демонстратором технологий. В Starter Pack обкатываются самые свежие версии библиотек перед тем, как будут перенесены в свои отдельные репозитории. Код экспериментальных версий библиотек находится в каталоге [repository_template/src/.contrib-candidates](repository_template/src/.contrib-candidates).

## Ключевые технологии

Шаблон веб-приложения опирается на стандартный для проектов Девмана стек технологий:

- Docker
- Kubernetes
- Менеджер зависимостей [Poetry](https://python-poetry.org/)
- Фреймворк [Django](https://www.djangoproject.com/)
- Библиотека [Tg API](https://gitlab.levelupdev.ru/dvmn-open-source-dev-tools/tg_api)
- Библиотека [HTTPX](https://www.python-httpx.org/)
- Библиотека [Pydantic](https://docs.pydantic.dev/latest/)
- Библиотека [Pytest](https://docs.pytest.org/en/latest/)
- Линтер flake8
- PostgreSQL
- [S3-compatible storage](https://cloud.yandex.ru/docs/glossary/s3)
- Сборщик логов [Rollbar](https://rollbar.com/)

## Реализованный функционал

Что полезного реализовано в StarterPack

- ПО полностью докеризировано
- В README написаны инструкции по развёртыванию проекта у себя на компьютере
- Настроены линтеры и EditorConfig
- Написаны первые автотесты на pytest с запросами к БД из Django ORM
- Подготовлены манифесты для запуска ПО в Kubernetes
- Реализован простой чат-бот на базе Django Tg Bot Framework
- К чат-боту подключен трекинг воронок
- В Django подключены:
    - кастомная модель пользователя
    - boto3 для работы с S3
    - сбор логов в Rollbar
    - другие полезные батарейки, см файл [settings.py](repository_template/src/project/settings.py)

## С чего начать

Сначала скопируйте содержимое каталога `repository_template` в корень своего нового проекта, затем пройдитесь по файлам и удалите лишний функционал, поправьте конфигурацию под свою задачу.

Не забудьте:

- Поправить название приложения в README
- Заменить в деплойных скриптах необходимые параметры для развертывания:
    - [.gitlab-ci.yml](repository_template/.gitlab-ci.yml)
    - [.deploy/](repository_template/.deploy)
