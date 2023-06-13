# Importamos las librerías
import pandas as pd 
import numpy as np
import sklearn
from fastapi import FastAPI
from sklearn.tree import DecisionTreeRegressor

# Indicamos título y descripción de la API
app = FastAPI(title='PROYECTO INDIVIDUAL Nº1  - Pia Castillo Areco DT11')

# Leer el archivo CSV 

url = https://raw.githubusercontent.com/piacastilloareco/peliculas_recomendacion/master/new_df.csv
df = pd.read_csv(url)
url2 = https://raw.githubusercontent.com/piacastilloareco/peliculas_recomendacion/master/new_df2.csv
df2 = pd.read_csv(url2)
url3 = https://raw.githubusercontent.com/piacastilloareco/peliculas_recomendacion/master/new_df3.csv
df3 = pd.read_csv(url3)
url4 = https://raw.githubusercontent.com/piacastilloareco/peliculas_recomendacion/master/dummy.csv
df_encoded = pd.read_csv(url4)

# Función de películas por mes

@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes:str):
    # Filtrar las filas que corresponden al mes especificado (aceptar el mes sin comillas)
    peliculas_mes = df[df['release_month'].str.lower() == mes.lower()]

    # Crear una lista de IDs únicos de películas
    ids_unicos = peliculas_mes['id'].unique()

    # Contar la cantidad de películas distintas
    cantidad_peliculas = len(ids_unicos)

    return {'mes':mes, 'cantidad':cantidad_peliculas}


# Función de películas por dia
@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia:str):
    # Filtrar las filas que corresponden al dia especificado
    peliculas_dia = df[df['day_of_week'].str.lower() == dia.lower()]

    # Crear una lista de IDs únicos de películas
    ids_unicos = peliculas_dia['id'].unique()

    # Contar la cantidad de películas distintas
    cantidad_peliculas = len(ids_unicos)

    return {'dia':dia, 'cantidad':cantidad_peliculas}


#Popularidad por pelicula 
@app.get('/score_titulo/{titulo}')
def score_titulo(titulo:str):
    # Filtrar el DataFrame para obtener la fila correspondiente al título de la película
    pelicula = df[df['title'] == titulo]

    if pelicula.empty:
        return "No se encontró información para la película:", titulo, "Por favor controla que estas escribiendo bien"

    # Obtener el año de estreno y la popularidad de la película
    release_year = pelicula['release_year'].values[0]
    popularity = pelicula['popularity'].values[0]

    return {'titulo':titulo, 'año': round(release_year), 'popularidad':popularity}


#Popularidad , Año de estreno y promedio de votos por pelicula 

@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo:str):
    # Filtrar el DataFrame para obtener la fila correspondiente al título de la película
    pelicula = df[df['title'] == titulo]

    if pelicula.empty:
        return "No se encontró información para la película:", titulo

    # Obtener el año de estreno y la popularidad de la película
    release_year = pelicula['release_year'].values[0]
    vote_count = pelicula['vote_count'].values[0]
    vote_average = pelicula['vote_average'].values[0]

    if vote_count >= 2000:
        return {'titulo':titulo, 'año':round(release_year), 'voto_total':vote_count, 'voto_promedio':vote_average}
    
    else:
        return f"La película {titulo} no cumple con la cantidad mínima de valoraciones requerida."
    

#Informacion Actor 
@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor:str):    
    # Reemplazar los valores nulos en la columna 'name_cast' con una cadena única
    df2['name_cast'] = df2['name_cast'].fillna('No disponible')

    # Filtrar las filas que contienen el nombre en la columna 'name_cast'
    peliculas_nombre = df2[df2['name_cast'].str.contains(nombre_actor, case=False, regex=False)]

    # Obtener la cantidad de películas
    cantidad_peliculas = peliculas_nombre['id'].nunique()

    # Obtener la suma de los retornos
    suma_retornos = peliculas_nombre['return'].sum()

    # Obtener el promedio de los retornos
    promedio_retornos = peliculas_nombre['return'].mean()

    return {'actor':nombre_actor, 'cantidad_filmaciones':cantidad_peliculas,'retorno_total' : suma_retornos, 'retorno_promedio':promedio_retornos}


#Informacion Director
@app.get('/get_director/{nombre_director}')
def get_director(nombre_director:str):
    # Reemplazar los valores nulos en la columna 'name_crew' con una cadena única
    df3['name_crew'] = df3['name_crew'].fillna('No disponible')

    # Filtrar las filas que contienen el nombre en la columna 'name_crew'
    peliculas_nombre = df3[df3['name_crew'].str.contains(nombre_director, case=False, regex=False)]

    # Obtener la cantidad de películas
    cantidad_peliculas = peliculas_nombre['id'].nunique()

    # Obtener la suma de los retornos
    suma_retornos = peliculas_nombre.groupby('id')['return'].sum().sum()

    # Crear un DataFrame con el título, la fecha de lanzamiento, el retorno, el costo y la ganancia de las películas
    df_peliculas = peliculas_nombre.drop_duplicates(subset='id')[['title', 'release_date', 'return', 'budget', 'revenue']].reset_index(drop=True)
   
    # Crear un diccionario con los resultados
    resultado = {
        'nombre_director': nombre_director,
        'retorno_total_director': suma_retornos,
        'peliculas': df_peliculas.to_dict(orient='records')
    }

    return resultado

@app.get('/get_recomendacion/{title}')
def recomendacion(title: str, n: int = 5):
    url4 = https://raw.githubusercontent.com/piacastilloareco/peliculas_recomendacion/master/dummy.csv
    df_encoded = pd.read_csv(url4)    
    
    # Paso 2: Filtrar las películas que comparten al menos dos géneros con la película de referencia
    generos_pelicula_referencia = df_encoded[df_encoded['title'] == title].drop(['title', 'vote_average'], axis=1)

    # Verificar si se encontró la película de referencia
    if generos_pelicula_referencia.empty:
        raise ValueError("La película de referencia no se encuentra en el dataset.")
    else:
        generos_pelicula_referencia = generos_pelicula_referencia.iloc[0]

    # Filtrar los valores no finitos y convertir los géneros a enteros
    generos_pelicula_referencia = generos_pelicula_referencia.replace([np.inf, -np.inf], np.nan).dropna().astype(int)

    # Obtener la cantidad de géneros compartidos por película
    generos_compartidos = df_encoded.iloc[:, 2:-1].apply(lambda x: sum((x.replace([np.inf, -np.inf], np.nan).dropna().astype(int) & generos_pelicula_referencia) >= 1), axis=1)

    # Filtrar las películas similares que comparten al menos dos géneros con la película de referencia
    peliculas_similares = df_encoded[generos_compartidos >= 2]

    # Verificar si se encontraron películas similares
    if peliculas_similares.empty:
        return {"message": "No se encontraron películas similares."}
    else:
        # Paso 3: Crear una lista con las características de la película de referencia
        caracteristicas_referencia = generos_pelicula_referencia.values.reshape(1, -1)

        # Paso 4: Obtener las características de las películas similares
        X = peliculas_similares.drop(['title', 'vote_average'], axis=1)
        y = peliculas_similares['vote_average']

        # Paso 5: Crear y entrenar el modelo de árbol de decisión
        model = DecisionTreeRegressor()
        model.fit(X, y)

        # Paso 6: Realizar la predicción utilizando el modelo de árbol de decisión
        predicciones = model.predict(caracteristicas_referencia)

        # Paso 7: Filtrar las películas similares con puntaje de votos igual o superior a la predicción
        peliculas_recomendadas = peliculas_similares[peliculas_similares['vote_average'] >= predicciones[0]]

        # Paso 8: Verificar si hay películas recomendadas
        if peliculas_recomendadas.empty:
            return {"message": "No se encontraron películas recomendadas."}
        else:
            # Paso 9: Ordenar las películas recomendadas por puntaje de votos de forma descendente
            peliculas_recomendadas = peliculas_recomendadas.sort_values(by='vote_average', ascending=False)

            # Paso 10: Tomar las primeras n películas recomendadas
            peliculas_recomendadas = peliculas_recomendadas.head(n)

            # Paso 11: Devolver la lista de películas recomendadas
            return peliculas_recomendadas['title'].tolist()

