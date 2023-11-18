# Development - Contributing

Большинство инструкций по работе с кодом Starter Pack собраны в файле [repository_template/README.md](repository_template/README.md), чтобы в свой новый проект прикладной программист вместе с кодом копировал и соотвествующую документацию. В том документе собран основной набор рекомендаций и инструкций, а ниже по тексту перечислены лишь те дополнения, которые необходимы разработчикам Starter Pack, но бесполезны для прикладных программистов — пользователей Starter Pack.

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

