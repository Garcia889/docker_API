# Utiliza la imagen base de PostgreSQL
FROM postgres:latest

# Variables de entorno para la configuración de PostgreSQL
ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_INITDB_ARGS "--auth-local=md5"

# Copia archivos o directorios necesarios al contenedor
#COPY init.sql /docker-entrypoint-initdb.d/
#COPY ./BD /ProyectoFinal/Credito_Default

# Puerto por defecto de PostgreSQL
EXPOSE 5432

# Comando para iniciar PostgreSQL al inicio del contenedor
CMD ["postgres"]
