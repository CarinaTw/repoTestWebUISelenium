# базовый образ
FROM python:3.8

# создание папки для тестов
RUN mkdir my_test_project

# рабочая директория
WORKDIR ./my_test_project
# копировать файлы из текущей рабочей директории в текущую директорию контейнера
COPY . .
# выполнить команды
RUN pip install -U pip
RUN pip install -r requirements.txt
# выполнить запуск тестов
#CMD ["pytest", "--alluredir", "allure-results"]
CMD ["python3", "tests/test_admin_login_page.py"]

1) Dockerfile создали, команды там прописали
2) Сбилдим имэдж -> docker build -t my_container_test docker_dir/
3) Проверим -> docker images
4) Делаем -> docker create my_container_test
5) Проверим -> docker ps -a
6) docker start -a container_id
=> в результате выполнится скрипт/тест внутри контейнера
