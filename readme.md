#  Proyecto Flask con Entorno de Desarrollo en Docker

Aplicación Flask minimalista con base de datos integrada (SQLite), preparada para desarrollo local rápido, testing automatizado y fácil onboarding de nuevos miembros del equipo. Consiste en un backend con diferentes rutas o solicitudes, entre las que se encuentran:
    -Añadir, modificar, eliminar nombres en una tabla de ejemplo.
    -Listar todas las tablas que se almacenan en la BBDD (por defecto solo hay una)
Los test se encuentran en su respectiva carpeta y prueban el alcance de al menos el 80% del código.

---

##  Requisitos previos

Asegúrate de tener instalado:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Jenkins, siguiendo los pasos que se indican en la siguiente web: https://www.jenkins.io/doc/book/installing/docker/ , además es necesario instalar los addons de git, aws, awscredential, docker y credentialbind.

---

## Clonar y levantar la aplicación localmente

```bash
git clone <URL_DEL_REPOSITORIO>
cd <nombre_del_repositorio>
docker-compose up --build

---

## Ejecución de test

```bash
docker-compose run app pytest

---

### Ver cobertura de test

```bash
docker-compose run app coverage run -m pytest
docker-compose run app coverage report -m

---

### Generar informe html con los test

```bash
docker-compose run app coverage html

---

# Normas de organización de ramas en el github

Usa ramas por funcionalidad: feature/<nombreDeLaFuncionalidadEnDesarrollo>

No hagas commits directos a main (despues de terminar el desarrollo se validara el merge con el main)

Todo nuevo código debe venir con su test correspondiente

Se debe mantener la cobertura por encima del 80%
