# Prometheus Metrics Microservice

Микросервис для экспорта Prometheus метрик с определением типа окружения.

## Быстрый запуск

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/vallomova/microservice-project)

## Метрики

После запуска в GitPod откроется браузер с микросервисом.

Доступные эндпоинты:
- `/` - главная страница
- `/metrics` - Prometheus метрики

Метрика `host_environment_type` показывает:
- `0` - физический сервер
- `1` - виртуальная машина  
- `2` - контейнер (значение в GitPod)

## Технологии

- Python 3
- Prometheus Client
- Ansible
- GitPod
