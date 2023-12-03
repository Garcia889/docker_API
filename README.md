# ITAM - Maestría en Ciencia de Datos - Otoño 2023
# Proyecto final Estadística Computacional : Default of Credit Card Taiwan 2005 Project

### Integrantes

|       Github User        |              Nombre               | Clave única |
| :---------------: | :-------------------------------: | ----------- |
| @ZaretCardenas |    Delia Zaret Cárdenas Modeno    |  20     |
|      @Daantge      | Daan Tonatiuh González Espinosa | 208809      |
|     @Garcia889     |      Ivan García Alba      | 214549      |
|    @vdr90     |    Valeria Durán Rubio     | 124273      |

### **Objetivo del proyecto**
Nuestro proyecto tiene como objetivo implementar un producto de datos tomando como base los datos de [Kaggle: Default Payments of Credit Card Clients in Taiwan from 2005] (https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients-dataset). Estos datos que tenemos fueron entrenados para generar un modelo de ML (con *Python*) que pueda regresar predicciones, generadas a través  de una tabla creada en *PosgresSQL* y que dichas predicciones puedan ser medidas en un dashboard de *Dash*, usando un API (*FastAPI*).

Este flujo descrito brevemente arriba, es totalmente reproducible por medio de Docker, el cual nos permite empaquetar cada paso del proyecto para que distintos usuarios puedan obtener el resultado final (**usuarios de Windows y MAC puede que necesiten usar diferentes comandos pero es igualmente reproducible**).

### **Problema de negocio**
Este proyecto tiene como finalidad ser un de ayuda para áreas técnicas, como la de un científico de datos, y no técnicas, como de negocio, que requieran tener un monitoreo de sus modelos en producción. Usando metricas para modelos clasificación e identificar si existe algún deterioro del modelo. 

¿Cómo lo hacemos? La funcionalidad de poder calcular la probabilidad de default de los clientes mediante un csv permite al usuario de la API tomar decisiones basadas en este output y decidir tomar medidas al respecto dependiendo del ciclo de vida del crédito en cuestión. Además, el dashboard final presenta visualmente el desempeño estadístico de la población de entrenamiento, test y nuevas observaciones para tener una mejor idea de la situación del modelo.
