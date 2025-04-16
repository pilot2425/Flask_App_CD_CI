# 🚀 Proyecto Flask con Entorno de Desarrollo en Docker

Aplicación Flask minimalista con base de datos integrada (SQLite), preparada para desarrollo local rápido, testing automatizado y fácil onboarding de nuevos miembros del equipo.

---

## 📦 Requisitos previos

Asegúrate de tener instalado:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## 🧱 Clonar y levantar la aplicación localmente

```bash
git clone <URL_DEL_REPOSITORIO>
cd <nombre_del_repositorio>
docker-compose up --build

## Ejecución de test

docker-compose run app pytest

### Ver cobertura de test
docker-compose run app coverage run -m pytest
docker-compose run app coverage report -m

### Generar informe html con los test
docker-compose run app coverage html

# Normas de organización de ramas en el github

Usa ramas por funcionalidad: feature/<nombreDeLaFuncionalidadEnDesarrollo>

No hagas commits directos a main (despues de terminar el desarrollo se validara el merge con el main)

Todo nuevo código debe venir con su test correspondiente

Se debe mantener la cobertura por encima del 80%
