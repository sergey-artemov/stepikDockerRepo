FROM --platform=linux/amd64 selenium/standalone-chrome:latest

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1

# Install Python and pip
USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Установка всех зависимостей проекта
WORKDIR /usr/src/app

# Копирование исходного кода проекта в образ
COPY test.py .
COPY requirements.txt .

RUN pip3 install -r requirements.txt

CMD ["python3", "./test.py"]