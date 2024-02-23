# Proyecto Django de Gestión de Usuarios y Dispositivos

Este proyecto Django utiliza el framework Django REST Framework (DRF) para proporcionar endpoints que permiten la autenticación de usuarios y la gestión de dispositivos. Se incluyen funciones para registrar nuevos usuarios, iniciar sesión, así como para listar, crear, actualizar y eliminar dispositivos. Además, se implementan funciones para realizar ping a dispositivos y registrar las ejecuciones correspondientes.

## Contenido
1. [Autenticación en Swagger](#autenticación-en-swagger)
2. [Autenticación de Usuarios](#autenticación-de-usuarios)
3. [Gestión de Dispositivos](#gestión-de-dispositivos)
4. [Ejecuciones de Dispositivos](#ejecuciones-de-dispositivos)
5. [Documentación con Swagger](#documentación-con-swagger)
6. [Protección CSRF](#protección-csrf)
7. [Cómo Iniciar el Proyecto](#cómo-iniciar-el-proyecto)

### Autenticación en Swagger

 **NOTA:** Al acceder a Swagger, se genera automáticamente una autenticación por defecto para probar los endpoints. Si intentas probar los endpoints con herramientas como Insomnia o Postman, deberás crear una sesión e iniciar sesión para obtener el token de autenticación.

### Autenticación de Usuarios

#### Registro de Usuarios

Para registrar un nuevo usuario, envía una solicitud POST con un JSON que contenga la información necesaria del usuario, incluyendo el correo electrónico y la contraseña.

#### Crear usuario
```
curl -X POST http://tu-servidor/api/signup/ -d '{"email": "nuevo_usuario@example.com", "password1": "tu_contraseña", "password2": "tu_contraseña"}' 
```

#### Inicio de Sesión

Para iniciar sesión, envía una solicitud POST con un JSON que contenga las credenciales del usuario.

```
curl -X POST http://tu-servidor/api/signin/ -d '{"username": "nombre_de_usuario", "password": "tu_contraseña"}'
```

### Gestión de Dispositivos

#### Lista de Dispositivos



Obtén una lista de todos los dispositivos registrados.
```
curl http://tu-servidor/api/devices/
```
#### Detalles de un Dispositivo

Obtén detalles de un dispositivo específico por su ID.

```
curl http://tu-servidor/api/devices/{device_id}/
```
#### Crear un Nuevo Dispositivo

Crea un nuevo dispositivo enviando una solicitud POST con un JSON que contenga los detalles del dispositivo.

```
curl -X POST http://tu-servidor/api/devices/create/ -d '{"name": "Nuevo Dispositivo", "ip_address": "192.168.1.1"}'
```
#### Actualizar un Dispositivo

Actualiza un dispositivo existente enviando una solicitud PUT con un JSON que contenga los datos actualizados.

```
curl -X PUT http://tu-servidor/api/devices/{device_id}/update/ -d '{"name": "Nuevo Nombre", "ip_address": "192.168.1.2"}'
```
#### Eliminar un Dispositivo

Elimina un dispositivo existente por su ID.

```
curl -X DELETE http://tu-servidor/api/devices/{device_id}/delete/
```

## Ejecuciones de Dispositivos
### Lista de Ejecuciones

Obtén una lista de todas las ejecuciones de dispositivos registradas.

```

curl http://tu-servidor/api/device-executions/
```
#### Detalles de una Ejecución

Obtén detalles de una ejecución de dispositivo específica por su ID.

```
curl http://tu-servidor/api/device-executions/{execution_id}/
```
#### Realizar Ping a un Dispositivo

Realiza un ping a un dispositivo por su ID y registra los resultados de la ejecución.

```
curl -X POST http://tu-servidor/api/devices/{device_id}/ping/
```

## Documentación con Swagger

La documentación detallada de la API se encuentra disponible en Swagger. Accede a http://tu-servidor/swagger/ para explorar los endpoints y realizar pruebas interactivas.

## Protección CSRF

Se ha implementado protección CSRF en algunos endpoints para garantizar la seguridad de las solicitudes.

## Cómo Iniciar el Proyecto

    Clona este repositorio.

    Instala las dependencias con pipenv install
    (asegúrate de tener pipenv instalado).

    Realiza las migraciones con pipenv run python
    manage.py migrate.

    Inicia el servidor de desarrollo con pipenv

    run python manage.py runserver.


Este README.md incluye instrucciones para instalar las dependencias con pipenv y algunos comandos actualizados. Asegúrate de tener pipenv instalado antes de seguir las instrucciones.

