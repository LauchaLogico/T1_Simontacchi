from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import hstack, csr_matrix
import pandas as pd
import numpy as np

app = FastAPI()

# Cargar el dataset (asegúrate de colocar la ruta correcta a tu archivo CSV)
df = pd.read_csv("Dataset/movies_api.csv")
df1 = pd.read_csv("Dataset/actores_api.csv")
df2 = pd.read_csv("Dataset/directores_api.csv")

# Convertir la columna de fechas a formato datetime y manejar valores NaT
df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
if df["release_date"].isna().any():
    print("Advertencia: Algunas fechas no se pudieron convertir y se establecieron como NaT.")

# Crear nombres de meses y días manualmente paraevitar incompatibilidades de idioma
meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

df["release_month"] = df["release_date"].dt.month.apply(lambda x: meses[x-1] if pd.notna(x) else None)
df["release_day"] = df["release_date"].dt.weekday.apply(lambda x: dias[x] if pd.notna(x) else None)

# API_Dia: pide un día de la semana y me da la cantidad de peliculas que se estrenaron ese día

@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    try:
        dia = dia.capitalize()
        if dia not in df["release_day"].unique():
            return {"mensaje": f"El día '{dia}' no se encuentra en el dataset. Asegúrate de usar el nombre correcto en español. Por Ejemplo: Lunes"}
        cantidad = df[df["release_day"] == dia].shape[0]
        return {"mensaje": f"{cantidad} películas fueron estrenadas el día {dia}"}
    except Exception as e:
        return {"error": f"Ocurrió un error: {str(e)}"}

# API_Mes: Me pide un mes y me da la cantidad de peliculas que se estrenaron ese mes

@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    try:
        mes = mes.capitalize()
        if mes not in df["release_month"].unique():
            return {"mensaje": f"El mes '{mes}' no se encuentra en el dataset. Asegúrate de usar el nombre correcto en español. Por Ej: Enero"}
        cantidad = df[df["release_month"] == mes].shape[0]
        return {"mensaje": f"En {mes} se estrenaron {cantidad} de películas"}
    except Exception as e:
        return {"error": f"Ocurrió un error: {str(e)}"}

# API_Actores: que pide el nombre de un actor y me da las peliculas y el retorno

@app.get("/get_actor/{nombre_actor}")
def get_actor1(nombre_actor: str):
    try:
        # Filtrar películas del actor en el dataset principal
        films_actor = df1[df1["name"].str.contains(nombre_actor, na=False)]
        cantidad = films_actor.shape[0]

        if cantidad == 0:
            return {"mensaje": f"El actor {nombre_actor} no se encuentra en el dataset."}

        # Hacer un merge entre df1 (películas) y df (detalles adicionales) basado en los IDs
        films_with_returns = films_actor.merge(df, left_on="id_original", right_on="id", how="inner")
        
        # Calcular el retorno total y promedio
        retorno_total = films_with_returns["return"].sum()
        retorno_promedio = retorno_total / cantidad

        return {
            "mensaje": f"El actor {nombre_actor} ha participado de {cantidad} filmaciones. "
                       f"Ha conseguido un retorno total de {retorno_total:.2f} con un promedio de {retorno_promedio:.2f} por filmación."
        }
    except Exception as e:
        return {"error": f"Ocurrió un error: {str(e)}"}

#API_Director: me pide el nombre de un director y me devuelve las peliculas que filmo

@app.get("/get_director/{nombre_director}")
def get_director(nombre_director: str):
    try:
        films = df2[df2["name"] == nombre_director]
        
        
        if films.empty:
            return {"mensaje": f"El director '{nombre_director}' no se encuentra en el dataset."}
        resultados = []

        # Hacer un merge entre df2 (películas) y df (detalles adicionales) basado en los IDs
        films_with_returns = films.merge(df, left_on="id_original", right_on="id", how="inner")
        films_with_returns = films_with_returns.sort_values(by='title')
        for _, film in films_with_returns.iterrows():
            resultados.append({
                "titulo": film["title"],
                "fecha_lanzamiento": film["release_date"],
                "retorno": film["return"],
                "costo": film["budget"],
                "ganancia": film["revenue"]
            })
        return {
            "mensaje": f"El director {nombre_director} ha dirigido {len(resultados)} filmaciones.",
            "detalladas a continuacion": resultados
        }
    except Exception as e:
        return {"error": f"Ocurrió un error: {str(e)}"}

#API_Titulo: me pide el tituo de una pelicula y me devuelve el año de estreno y el retorno

@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str):
    try:
        film = df[df["title"] == titulo].iloc[0]
        return {
            "mensaje": f"La película {titulo} fue estrenada en el año {film['release_year']} con una popularidad de {film['popularity']}"
        }
    except IndexError:
        return {"mensaje": f"La película '{titulo}' no se encuentra en el dataset."}
    except Exception as e:
        return {"error": f"Ocurrió un error: {str(e)}"}

#API_votos: me pide el titulo y me devuelve el año de estreno, los votos y la valoración
@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str):
    try:
        film = df[df["title"] == titulo].iloc[0]
        if film["vote_count"] >= 2000:
            promedio = film["vote_average"]
            return {
                "mensaje": f"La película {titulo} fue estrenada en el año {film['release_year']}. La misma cuenta con un total de {film['vote_count']} valoraciones, con un promedio de {film['vote_average']}"
            }
        else:
            return {"mensaje": f"La película {titulo} tiene menos de 2000 valoraciones."}
    except IndexError:
        return {"mensaje": f"La película '{titulo}' no se encuentra en el dataset."}
    except Exception as e:
        return {"error": f"Ocurrió un error: {str(e)}"}

# API Recomendaciones
#Definir modelos para la API
class RecommendationRequest(BaseModel):
    title: str
    n: int = 5

class ConfigurableNN:
    def __init__(self, metric="cosine", algorithm="auto"):
        self.nn = NearestNeighbors(metric=metric, algorithm=algorithm)

    def fit(self, features):
        self.nn.fit(features)

    def kneighbors(self, feature, n_neighbors=5):
        return self.nn.kneighbors(feature, n_neighbors=n_neighbors)

# Cargar y procesar los datasets
movies_api = pd.read_csv("Dataset/recomendacion_api.csv")
genres_data = pd.read_csv("Dataset/genres_api.csv")

movies_api["id"] = movies_api["id"].astype(str)
genres_data["id_original"] = genres_data["id_original"].astype(str)

movies_with_genres = pd.merge(movies_api, genres_data, left_on="id", right_on="id_original", how="left")

movies_with_genres = movies_with_genres.groupby("id_original").agg({
    "title": "first",
    "name": lambda x: " ".join(set(x.dropna())),
    "vote_average": "first",
    "popularity": "first"
}).reset_index()

movies_with_genres["combined_features"] = (
    movies_with_genres["title"].fillna("") + " " +
    movies_with_genres["name"].fillna("")
)

tfidf = TfidfVectorizer(stop_words="english", max_features=5000)
tfidf_matrix = tfidf.fit_transform(movies_with_genres["combined_features"])

scaler = MinMaxScaler()
movies_with_genres[["vote_average", "popularity"]] = scaler.fit_transform(
    movies_with_genres[["vote_average", "popularity"]]
)

numerical_features = csr_matrix(movies_with_genres[["vote_average", "popularity"]].values)

final_features = hstack([tfidf_matrix, numerical_features])

# Instancia configurable de NearestNeighbors
nn = ConfigurableNN(metric="cosine", algorithm="auto")
nn.fit(final_features)

# Función para encontrar películas similares
def find_similar_movies(title, n=5):
    if title not in movies_with_genres["title"].values:
        raise ValueError(f"La película '{title}' no se encontró en la base de datos.")

    idx = movies_with_genres[movies_with_genres["title"] == title].index[0]
    distances, indices = nn.kneighbors(final_features[idx], n_neighbors=n+1)
    recommended_titles = movies_with_genres.iloc[indices[0]]['title'].tolist()
    recommended_titles = [t for t in recommended_titles if t != title]

    # Rellenar con títulos adicionales si faltan recomendaciones
    if len(recommended_titles) < n:
        extra_titles = movies_with_genres[~movies_with_genres["title"].isin(recommended_titles + [title])]["title"].tolist()
        recommended_titles.extend(extra_titles[:n - len(recommended_titles)])

    return recommended_titles[:n]

# Endpoints de la API
@app.get("/")
def root():
    return {"message": "Bienvenido a la API de recomendación de películas."}

@app.post("/recommendations/")
def get_recommendations(request: RecommendationRequest):
    try:
        if not request.title:
            raise HTTPException(status_code=400, detail="El título de la película es obligatorio.")
        recommendations = find_similar_movies(request.title, request.n)
        return {"title": request.title, "recommendations": recommendations}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor.")
