FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update \
    && apt-get install -y libmariadb-dev \
    && apt-get install -y python3-pip \
    && apt-get install -y build-essential \
    && apt-get install -y libcurl4-openssl-dev \
    && apt-get install -y libssl-dev \
    && pip install --upgrade pip

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el contenido del directorio actual al contenedor en /app
COPY . /app

# Instala las dependencias con Pipenv
RUN pip install pipenv && pipenv install

# Expone el puerto 8000
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
