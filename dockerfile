FROM python:3.11

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el Pipfile y Pipfile.lock al contenedor
COPY Pipfile Pipfile.lock /app/

# Instala pipenv si no está instalado
RUN which pipenv || pip install pipenv

# Instala las dependencias con Pipenv, incluyendo Django
RUN pipenv install --deploy --ignore-pipfile

# Instala el paquete ping (iputils-ping) necesario
RUN apt-get update && apt-get install -y iputils-ping

# Copia el contenido del directorio actual al contenedor en /app
COPY . /app/

# Expone el puerto 8000
EXPOSE 8000

# Comando para activar el entorno virtual y ejecutar la aplicación
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
