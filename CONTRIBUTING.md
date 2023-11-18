# Development - Contributing

Большинство инструкций по работе с кодом Starter Pack собраны в файле [repository_template/README.md](repository_template/README.md), чтобы в свой новый проект прикладной программист вместе с кодом копировал и соотвествующую документацию. В том документе собран основной набор рекомендаций и инструкций, а ниже по тексту перечислены лишь те дополнения, которые необходимы разработчикам Starter Pack, но бесполезны для прикладных программистов — пользователей Starter Pack.

<a name="local-setup"></a>
## Как развернуть local-окружение

В репозитории Start Pack используются хуки pre-commit, чтобы автоматически запускать линтеры и автотесты. Хуками управляет файл `.pre-commit-config.yaml`, и в репозитории он существует сразу в двух копиях: файл в каталоге `repository_template` копируется вместе с кодом в новые проекты, а файл в корне репозитория используют разработчики самого Starter Pack.

Для разработки Starter Pack вам нужно деактивировать файл `.pre-commit-config.yaml` внутри каталога `repository_template` и активировать одноимённый файл в корне репозитория:

```shell
$ cd repository_template
$ pre-commit uninstall
$ cd ../
$ pre-commit install
```

<a name="run-python-linters"></a>
### Как запустить линтеры Python

Чтобы подсветить ошибки форматирования кода внутри Sublime Text используйте настройки с указанием пути к файлу `repository_template/docker-compose.yml`:

```jsonc
// project settings file
{
    "settings": {
        // specify folder where docker-compose.yaml file placed to be able to launch `docker compose`
        "SublimeLinter.linters.flake8.working_dir": "/path/to/repo/",
        "SublimeLinter.linters.flake8.executable": ["docker", "compose", "-f", "repository_template/docker-compose.yml", "run", "--rm", "linters", "flake8"],
    },
}
```

