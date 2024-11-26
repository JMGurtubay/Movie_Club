
# 🎬 Movie Club Management System

## Descripción del Proyecto

**Movie Club Management System** es una aplicación diseñada para un club de cinéfilos. Este sistema permite a los usuarios gestionar películas y reservar salas de proyección o *movie theaters*. Está diseñado para ser práctico, eficiente y fácil de usar, facilitando la organización de proyecciones para los miembros del club.

Con esta plataforma, los usuarios pueden:
- Agregar y gestionar películas.
- Consultar salas de proyección disponibles.
- Realizar y gestionar reservas en las salas de proyección.

La aplicación está desarrollada utilizando **FastAPI** para el backend y una base de datos **MongoDB**.

---

## Funcionalidades Principales

- **Gestión de Películas**: Crear, consultar, actualizar y eliminar películas del catálogo.
- **Gestión de Salas**: Ver la disponibilidad de salas y detalles como capacidad máxima y características técnicas.
- **Reservas**: Realizar reservas de salas de proyección y asegurarse de que no haya conflictos de horario.
- **Integración de API**: Documentación automática y endpoints listos para pruebas con Swagger UI.

---

## 🛠️ Requisitos para Configuración

### Antes de comenzar, asegúrate de tener instalado:

- **Docker Desktop** (para sistemas Windows o macOS) o **Docker Engine** (para WSL en Linux).  
  [Guía de instalación de Docker](https://docs.docker.com/get-docker/).

---

## 🚀 Pasos para Configurar y Probar la Aplicación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/JMGurtubay/Movie_Club.git
cd Movie-Club
```

### 2. Configurar Docker Desktop o Docker Engine

#### **Docker Desktop (Windows/macOS)**:
1. Abre Docker Desktop y asegúrate de que está corriendo.
2. Ve a la configuración y habilita **WSL Integration** (si estás en Windows con WSL).
3. Confirma que Docker está funcionando ejecutando:
   ```bash
   docker --version
   ```

#### **Docker Engine (Linux/WSL)**:
1. Instala Docker Engine:
   ```bash
   sudo apt-get update
   sudo apt-get install docker.io
   ```
2. Activa y verifica el servicio:
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   docker --version
   ```

---

### 3. Construir y Levantar el Contenedor

En el directorio raíz del proyecto (`movie-club`), ejecuta los siguientes comandos:

1. **Construir y levantar los servicios**:
   ```bash
   docker compose up --build
   ```

2. **Verificar que los contenedores estén corriendo**:
   ```bash
   docker ps
   ```

---

### 4. Probar las apis con pytest
1. Entrar al contenedor tanto del backend como de Mongo
   ```bash
   docker ps
   ```
   ```bash
   docker exec -it [id_cont] bash
   ```

2. Dentro del contenedor del backend corre el pytests
   ```bash
   pytests app/tests/movies_test.py
   ```
    ```bash
   pytests app/tests/theater_test.py
   ```
   ```bash
   pytests app/tests/users_test.py
   ```
   ```bash
   pytests app/tests/reservations_test.py
   ```

   IMPORTANTE!! Es probable que al tratar de hacer el pytests de users no pasen todas las pruebas porque hay validaciones que no permites crear usuarios con el mismo nombre o email

   Para resovlerlos una vez dentro del contenedor:
   Entrar al mongo shell
   ```bash
   mongosh
   ```
   Entrar a la base de datos
   ```bash
   use movie_club
   ```
   Hacer un drop de de la coleccion de users
   ```bash
   db.users.drop()
   ```

   Volver a ejectutar el pytest de users
   ```bash
   pytests app/tests/users_test.py
   ```
   
### 5. Probar las apis desde el navegador
1. Si decidiste correr los contenedores desde sl subsistema de linux WSL primero debes de obtener la ip del subsistema
   ```bash
   hostname -I
   ```
   La primer ip que aparezca es la que necesitamos, copiala y pegala en el navegador junto con el puerto :8000 y el endpoint de la documentacion de OpenAPI /docs

   Si decidiste hacerlo desde Docker Desktop no necesitas obtener la ip, unicamente coloca localhost en el navegador junto con el puerto y el endpoint

3. Dejo un ejemplo para ver como se veria la url del navegador 
    http://localhost:8000/docs
    http://172.25.106.67:8000/docs
---

### 6. Detener los Contenedores

Para detener los contenedores sin eliminar los datos:

```bash
docker compose down
```

Para detenerlos y eliminar los datos del contenedor (como la base de datos MongoDB):

```bash
docker compose down -v
```

---

## 📝 Notas Adicionales

- La base de datos MongoDB se almacena en un volumen persistente, lo que significa que los datos no se pierden al detener los contenedores.
- Si tienes problemas con permisos en Docker en WSL, asegúrate de que tu usuario pertenezca al grupo `docker`:
  ```bash
  sudo usermod -aG docker $USER
  ```

---

¡Gracias por explorar este proyecto! Si tienes preguntas o sugerencias, no dudes en abrir un **Issue** en este repositorio. 🎉
