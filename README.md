Machine Learning Operations (MLOps)
Este proyecto abarca una serie de pasos para desarrollar un proceso de Data Engineering sobre un dataset de películas, con el objetivo de disponibilizar una serie de endpoints y un modelo de recomendación de películas utilizando Machine Learning a través de una API.

Contexto
Se plantea la necesidad desde los departamentos de Machine Learning y Analytics de contar con los datos en una API para poder ser consumidos. Además, se requiere realizar consultas al modelo de recomendación, lo cual implica hacer un despliegue (deploy) de la API.

Dataset
El dataset utilizado contiene información acerca de películas y distintos atributos relacionados. Se dispone de los siguientes conjuntos de datos:

1) New_df: es un dataframe que cuenta con 11 columnas y permite analizar las características comunes de las películas, reduciendo el tamaño de los registros.
2) New_df2: es un dataframe que cuenta con 3 columnas y está orientado al estudio del elenco que trabajó en las películas.
3) New_df3: es un dataframe que cuenta con 3 columnas y está orientado al estudio del cuerpo de directores que intervienen en el desarrollo de las películas.
4) Dummy.csv: es una dummy que nos permite estudiar los diferentes géneros en los que se pueden categorizar las películas, y es fundamental para el sistema de recomendación.
5) Merge_df: es un dataframe que cuenta con 13 columnas y se utiliza para el análisis exploratorio de los datos.


Data Engineering
Para el trabajo de Data Engineering se llevaron a cabo una serie de transformaciones sobre los datos, que incluyeron:
 - Desanidamiento de algunos campos para poder utilizarlos en el análisis exploratorio de los datos y las consultas requeridas.
 - Rellenado de valores nulos en los campos revenue y budget con el número 0.
 - Eliminación de valores nulos en el campo release date.
 - Modificación del formato de las fechas al formato AAAA-mm-dd.
 - Creación de un campo release_year que extrae el año de estreno de las películas.
 - Creación de un campo release_day que extrae el día de estreno de las películas.
 - Creación de un campo release_month que extrae el mes de estreno de las películas.
 - Creación de la columna return que calcula el retorno de inversión dividiendo los campos revenue y budget. Cuando no hay datos disponibles para calcularlo, se toma el valor 0.
 - Eliminación de las columnas que no serán utilizadas, como: video, imdb_id, adult, original_title, vote_count, poster_path y homepage.
 - Las transformaciones y los análisis realizados se pueden visualizar en el siguiente archivo.

API
Se han implementado los siguientes endpoints a través del Framework FastAPI:

cantidad_filmaciones_mes(Mes): Recibe un mes en idioma Español y devuelve la cantidad de películas estrenadas en ese mes en el conjunto de datos. Ejemplo de retorno: "X cantidad de películas fueron estrenadas en el mes de X".

cantidad_filmaciones_dia(Dia): Recibe un día en idioma Español y devuelve la cantidad de películas estrenadas en ese día en el conjunto de datos. Ejemplo de retorno: "X cantidad de películas fueron estrenadas en los días X".

score_titulo(titulo_de_la_filmación): Recibe el título de una filmación y devuelve el título, el año de estreno y el score/popularidad. Ejemplo de retorno: "La película X fue estrenada en el año X con un score/popularidad de X".

votos_titulo(titulo_de_la_filmación): Recibe el título de una filmación y devuelve el título, la cantidad de votos y el valor promedio de las votaciones. La película debe tener al menos 2000 valoraciones; en caso contrario, se devuelve un mensaje indicando que no cumple esta condición y no se devuelve ningún valor. Ejemplo de retorno: "La película X fue estrenada en el año X. La misma cuenta con un total de X valoraciones, con un promedio de X".

get_actor(nombre_actor): Recibe el nombre de un actor presente en el dataset y devuelve su éxito medido a través del retorno, la cantidad de películas en las que ha participado y el promedio de retorno. No se consideran directores en esta definición. Ejemplo de retorno: "El actor X ha participado en X cantidad de filmaciones, obteniendo un retorno de X con un promedio de X por filmación".

get_director(nombre_director): Recibe el nombre de un director presente en el dataset y devuelve su éxito medido a través del retorno, junto con el nombre de cada película, la fecha de lanzamiento, el retorno individual, el costo y la ganancia.

Análisis exploratorio de datos
Se realizaron análisis y estudios sobre las variables del dataset para comprender la relevancia de los datos y encontrar relaciones entre ellos. Los análisis incluyeron distribuciones de frecuencia de variables numéricas, identificación de variables categóricas y sus valores, correlación entre variables, análisis temporal y por categoría. Se realizaron algunas transformaciones adicionales diferentes a las de la sección de Data Engineering. Los detalles de las transformaciones y los análisis realizados se pueden encontrar en el siguiente archivo.

Modelo de recomendación - Machine Learning
El modelo propuesto es un sistema de recomendación de películas basado en la similitud de géneros y puntajes de votos. El flujo del modelo es el siguiente:

1) Se parte de un DataFrame df_encoded que contiene la información de las películas previamente codificada.
2) Se especifica una película de referencia pelicula_referencia. Se buscan las películas del DataFrame que comparten al menos dos géneros con la película de referencia.
3) Se crean las características de la película de referencia, que corresponden a los géneros codificados en formato de vector.
4) Se obtienen las características de las películas similares, excluyendo las columnas de título y puntaje de votos.
5) Se crea y entrena un modelo de regresión de árbol de decisión utilizando las características de las películas similares y sus puntajes de votos.
6) Se realiza la predicción utilizando el modelo entrenado con las características de la película de referencia.
7) Se filtran las películas similares que tienen un puntaje de votos igual o superior a la predicción realizada.
8) Se verifica si hay películas recomendadas según los criterios establecidos.
9) Se ordenan las películas recomendadas por puntaje de votos de forma descendente.
10) Se seleccionan las primeras n películas recomendadas (en este caso, n se establece como 5).
11) Se devuelve una lista con los títulos de las películas recomendadas.

Deployment
Para el despliegue de la API, se utilizó la plataforma Render. Los datos están listos para ser consumidos y consultados a través del siguiente enlace:
Para el despliegue de la API, se utilizó la plataforma Render. Los datos están listos para ser consumidos y consultados a través del siguiente enlace:
