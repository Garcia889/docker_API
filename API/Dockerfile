# Usamos imagen de Python
FROM python:3.9-slim

# Establecemos el directorio de trabajo del contenedor
WORKDIR /app

# Copiamos el contenido del directorio actual a /app
COPY . /app

# Instalamos paquetes especificados en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exponemos puerto 8000
EXPOSE 8000

# Define environment variable
# ENV NAME World

# Iniciamos servicio de Fast API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
