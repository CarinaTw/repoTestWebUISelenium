# базовый образ
FROM python:3.8

# создание папки для тестов
RUN mkdir repoTestWebUISelenium
RUN cd repoTestWebUISelenium

# копировать файлы из текущей рабочей директории в текущую директорию контейнера
COPY . ./repoTestWebUISelenium

# рабочая директория
WORKDIR /repoTestWebUISelenium

# выполнить команды
RUN pip install -U pip
RUN pip install -r requirements.txt

# выполнить запуск тестов
#CMD ["python3", "tests/test_admin_login_page.py"]

