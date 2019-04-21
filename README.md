### Переменные окружения
* SECRET_KEY - приватный ключ
* PUBLIC_KEY - публичный ключ
* EMAIL_HOST - почтовый сервер
* EMAIL_PORT - порт почтового сервера
* EMAIL_HOST_USER - адрес почтового ящика, с которого будут рассылаться уведомления
* EMAIL_HOST_PASSWORD - пароль к почтовому ящику
* EMAIL_USE_TLS - используется ли почтовым сервером TLS (не указывать, если нет)
* EMAIL_USE_SSL - используется ли почтовым сервером SSL (не указывать, если нет)

### Запуск проекта
1. Создать окружение c Python 3.7, активировать его
2. Установить python-зависимости из `config/requirements.txt` (`pip install -r config/requirements.txt`)
3. Установить базу данных: `make local-up`
4. Перейти в папку `base_app`
4. Выполнить миграции: `python manage.py migrate`
5. Добавить переменные окружения (их можно сложить в файл `.env`)
6. В отдельной консоли запустить распределенную очередь заданий django-q: `python manage.py qcluster`
7. Запустить приложение: `python manage.py runserver`