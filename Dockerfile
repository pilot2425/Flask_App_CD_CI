FROM python:3.11-slim

# Evitar prompts durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Establece directorio de trabajo
WORKDIR /app

# Instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el proyecto
COPY . .

# Expone el puerto Flask
EXPOSE 5000

# Ejecuta la base de datos y la app
CMD ["sh", "-c", "python manage.py && python run.py"]
