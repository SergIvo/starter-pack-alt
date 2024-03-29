История изменений
===============

При очередном комите в файл записываем кратко смысл коммита, если были значимые изменения.

Изменения записываем в самый верх.

При публикации все изменения собираются в очередную версию.


Не в релизе
------------------------

- Удалил из README поломанные разделы по работе с дампом тестовой БД, убрал наработки в issue #104
- Добавлен файл `.pre-commit-config.yaml` для разработчиков Starter Pack
- Добавлен файл `CONTRIBUTING.md` для разработчиков Starter Pack
- В инструкции repository_template/README.md добавлен ранее пропущенный раздел про линтеры
- Уточнены названия скриптов `make`, добавлена встроенная справка
- Исправлены настройки EditorConfig для файлов Makefile из-за которых ломались символы TAB

### Update 2023-11-09

- Исправлен баг "В private_chat берется не тот ник пользователя" #37
- Добавлено новое отчуждаемое django-приложение [django_workers](repository_template/src/.contrib-candidates/django_workers/)
- Добавлен новый модуль [funnels](repository_template/src/.contrib-candidates/django_tg_bot_framework/funnels/) в Django Tg Bot Framework

### Update 2023-11-01

- django_tg_bot_framework/private_chats: исправлена ошибка вложенных транзакций
- Yostate: исправлен баг в методе `Locator.parse_obj`
- Добавлено django приложение `trigger_funnel`
- Перенастроено логирование в проекте Django, чтобы сообщения долетали до консоли

### Update 2023-10-09

- В Django Tg Bot Framework исправлен баг обработки событий `PrivateChatMessageEdited` и `PrivateChatCallbackQuery` - #35

### Update 2023-10-07

- Код внешней библиотеки Django Tg Bot Framework скопирован в репозиторий Devman Tg Bot Starter Pack в каталог .contrib-candidates
- Проведён глубокий рефакторинг Django Tg Bot Framework
- Часть кода Django Tg Bot Framework переехала в новый пакет Yostate

### Update 2023-10-03
- Шаблон проекта переехал в каталог `repository_template` - [#9](https://gitlab.levelupdev.ru/dvmn-open-source-dev-tools/devman-tg-bot-starter-pack/-/issues/9)
- Изменена документация - [#10](https://gitlab.levelupdev.ru/dvmn-open-source-dev-tools/devman-tg-bot-starter-pack/-/issues/10), [#11](https://gitlab.levelupdev.ru/dvmn-open-source-dev-tools/devman-tg-bot-starter-pack/-/issues/11), [#12](https://gitlab.levelupdev.ru/dvmn-open-source-dev-tools/devman-tg-bot-starter-pack/-/issues/12), [#13](https://gitlab.levelupdev.ru/dvmn-open-source-dev-tools/devman-tg-bot-starter-pack/-/issues/13), [#14](https://gitlab.levelupdev.ru/dvmn-open-source-dev-tools/devman-tg-bot-starter-pack/-/issues/14), [#15](https://gitlab.levelupdev.ru/dvmn-open-source-dev-tools/devman-tg-bot-starter-pack/-/issues/15), [#32](https://gitlab.levelupdev.ru/dvmn-open-source-dev-tools/devman-tg-bot-starter-pack/-/issues/32)
- Вернули файл .pre-commit-config.yml - [#25](https://gitlab.levelupdev.ru/dvmn-open-source-dev-tools/devman-tg-bot-starter-pack/-/issues/25)
- Решена проблема с миграциями - [#30](https://gitlab.levelupdev.ru/dvmn-open-source-dev-tools/devman-tg-bot-starter-pack/-/issues/30)
- Исправлен модуль с тестом - [#24](https://gitlab.levelupdev.ru/dvmn-open-source-dev-tools/devman-tg-bot-starter-pack/-/issues/24)
