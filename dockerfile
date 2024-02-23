FROM python:3.11

# Establece el directorio de trabajo en /app
WORKDIR /app

# Evita la generación de archivos bytecode y desactiva el almacenamiento en búfer
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copia el Pipfile y Pipfile.lock al contenedor
COPY Pipfile Pipfile.lock /app/

# Instala pipenv si no está instalado
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Instala el paquete ping (iputils-ping) necesario
RUN apt-get update && apt-get install -y iputils-ping

# Copia el contenido del directorio actual al contenedor en /app
COPY . /app/


# Expose port 8000 for the Django app
EXPOSE 8000

# Comando para activar el entorno virtual y ejecutar la aplicación
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
