FROM python:3.10

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el Pipfile y Pipfile.lock al contenedor
COPY Pipfile Pipfile.lock /app/

# Instala las dependencias con Pipenv
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Copia el contenido del directorio actual al contenedor en /app
COPY . /app/

# Expone el puerto 8000
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
