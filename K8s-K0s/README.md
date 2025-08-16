# Helm-чарты для DevOps-проекта

В этой директории находятся Helm-чарты для деплоя всех основных сервисов проекта в Kubernetes-кластер:

- flask-chart — Flask-приложение
- grafana-chart — Grafana (визуализация метрик и логов)
- prometheus-chart — Prometheus (мониторинг)
- loki-chart — Loki (логирование)
- promtail-chart — Promtail (агент сбора логов)
- postgres-chart — PostgreSQL (база данных)

---

## Структура каждого чарта

```
<service>-chart/
├── Chart.yaml           # Метаинформация Helm-чарта
├── values.yaml          # Основные параметры (образ, порты, переменные окружения)
└── templates/
    ├── deployment.yaml  # Deployment для сервиса
    ├── service.yaml     # Service для доступа к поду
    └── configmap.yaml   # (если нужно) Конфиг для сервиса
```

---

## Как установить сервис в кластер

1. Перейдите в папку с нужным чартом, например:
   ```bash
   cd K8s-K0s/flask-chart
   ```
2. Отредактируйте `values.yaml` под свои нужды (например, укажите свой образ).
3. Установите чарт:
   ```bash
   helm install <release-name> .
   # Например:
   helm install flask-app .
   ```
4. Проверьте, что поды и сервисы запущены:
   ```bash
   kubectl get pods
   kubectl get svc
   ```

---

## Пример values.yaml для Flask

```yaml
replicaCount: 1
image:
  repository: <ваш-dockerhub-логин>/flask-app
  tag: latest
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 5000
env:
  DB_HOST: "db"
  DB_NAME: "project1_db"
  DB_USER: "postgres"
  DB_PASSWORD: "yourpass"
  SECRET_KEY: "yourkey"
```

---

## Пример values.yaml для Prometheus

```yaml
replicaCount: 1
image:
  repository: prom/prometheus
  tag: v2.45.0
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 9090
configMap:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
      - job_name: 'flask'
        static_configs:
          - targets: ['flask-app:5000']
```

---

## Важно
- Для работы всех сервисов в одной сети используйте общую namespace или настройте networkPolicy.
- Для production-окружения обязательно используйте секреты для паролей и уникальные значения.
- Для Postgres рекомендуется подключить volume для хранения данных (можно добавить в deployment.yaml).

---

## Полезные команды

- Обновить релиз:
  ```bash
  helm upgrade <release-name> .
  ```
- Удалить релиз:
  ```bash
  helm uninstall <release-name>
  ```
- Просмотреть логи пода:
  ```bash
  kubectl logs <pod-name>
  ```

---

