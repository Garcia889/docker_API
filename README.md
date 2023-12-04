# ITAM - Maestría en Ciencia de Datos - Otoño 2023
## Proyecto final Estadística Computacional : Default of Credit Card Taiwan 2005

### Integrantes

|       Github User        |              Nombre               | Clave única |
| :---------------: | :-------------------------------: | ----------- |
| @ZaretCardenas |    Delia Zaret Cárdenas Modeno    |  208799     |
|      @Daantge      | Daan Tonatiuh González Espinosa | 208809      |
|     @Garcia889     |      Ivan García Alba      | 214549      |
|    @vdr90     |    Valeria Durán Rubio     | 124273      |

### **Objetivo del proyecto**
Nuestro proyecto tiene como objetivo implementar un producto de datos tomando como base los datos de [Kaggle: Default Payments of Credit Card Clients in Taiwan from 2005] (https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients-dataset). Estos datos que tenemos fueron entrenados para generar un modelo de ML (con *Python*) que pueda regresar predicciones, generadas a través  de una tabla creada en *PosgresSQL* y que dichas predicciones puedan ser medidas en un dashboard de *Dash*, usando un API (*FastAPI*).

Este flujo descrito brevemente arriba, es totalmente reproducible por medio de Docker, el cual nos permite empaquetar cada paso del proyecto para que distintos usuarios puedan obtener el resultado final (**usuarios de Windows y MAC puede que necesiten usar diferentes comandos pero es igualmente reproducible**).

### **Problema de negocio**
Este proyecto tiene como finalidad ser un de ayuda para áreas técnicas, como la de un científico de datos, y no técnicas, como de negocio, que requieran tener un monitoreo de sus modelos en producción. Usando metricas para modelos clasificación e identificar si existe algún deterioro del modelo. 

*¿Cómo lo hacemos?* La funcionalidad de poder calcular la probabilidad de default de los clientes mediante un csv permite al usuario de la API tomar decisiones basadas en este output y decidir tomar medidas al respecto dependiendo del ciclo de vida del crédito en cuestión. Además, el dashboard final presenta visualmente el desempeño estadístico de la población de entrenamiento, test y nuevas observaciones para tener una mejor idea de la situación del modelo.

### **Instalación**
1. Clona el repositorio

```bash
git clone git@github.com:vdr90/Credito_Default.git
cd Credito_Default
```

2. Descarga los archivos 

3. Abre la aplicación **Docker**

4. Construye y levanta los contenedores con Docker Compose
```bash
docker-compose up --build
```
Esto iniciará los servicios de FastAPI, Dash y PostgreSQL en contenedores separados.

5. Accede a la aplicación
* El dashboard Dash estará disponible en http://localhost:8050.
* La API FastAPI estará disponible en http://localhost:8000.

## Estructura del Proyecto:
La carpeta tiene una estructura de archivos dependiendo de la funcionalidad. Aquí se explica cómo funciona cada herramienta. 

* Interfaz de Programas de Aplicaciones (API)
  
  * **main.py:** Es la aplicación API de python con FastAPI  (dentro de carpeta **API**). Este script es la base de la aplicación. En donde se generan las predicciones y se conecta con las tablas de PosgresSQL.
    
  * **Readme.txt** Este archivo tiene la explicación de cómo correr FastAPI individualmente.
    
  * **DockerFile** Este archivo tiene la configuración de la imagen de docker de FastAPI para poder ser llamado con posterioridad y conectar las diferentes aplicaciones simultaneamente.
    
  * **estimator_hyper_xgb.joblib** Este archivo binario contiene al modelo de la librería XGBoost, desarrollado en python para obtener las predicciones.
    
  * **requirements.txt** Este archivo de texto contiene a todas las librerías necesarias para poder correr la API, y son instaladas durante la creación de la imagen de Docker de FastAPI.
 
* Base de Datos (BD)
  
  * **init_sql.sql:** script que construye la table de la base de datos (dentro de carpeta **BD**)
    
  * **DockerFile** Este archivo tiene la configuración de la imagen de la tabla de la base de datos creada en Posgres.

* Tablero (Dash)
  
  * **app.py:** Este script invoca a la API la cual crea una conexion a la base de datos de PosgresSQL y también calula la predicción estos datos se usan para poder generar el tablero con las gráficas y poblaciones seleccionadas (dentro de carpeta **Dash**).
    
  * **DockerFile** Este archivo tiene la configuración de la imagen de docker de dash para poder ser llamadoposteriormente y conectar las diferentes aplicaciones simultaneamente.
    
  * **requirements.txt** Este archivo de texto contiene a todas las librerías necesarias para poder correr el tablero, y son instaladas durante la creación de la imagen de Docker de dash.
 
* Unión de aplicaciones
  
  * **docker-compose.yaml:** script que corre la imagen del proyecto, postgres, FastAPI y Dash, para que todas estas se conecten y puedas obtener el resultado final.



##  Tecnologías utilizadas

* PostgreSQL
* Dash
* Python
* FastAPI
* Docker

## Librerías y Paquetes Utilizados

 - Leer requirements.txt

## Referencias 

* [FastAPI](https://fastapi.tiangolo.com/)
* [Docker](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
* [Python](https://www.python.org/)
* [Dash](https://dash.plotly.com/)
* [PostgreSQL](https://www.postgresql.org/)
