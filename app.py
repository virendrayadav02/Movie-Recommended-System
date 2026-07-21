import streamlit as st
import pickle
import pandas as pd
import requests


API_KEY = st.secrets["TMDB_API_KEY"]


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"

    except requests.exceptions.RequestException as e:
        print("TMDB Error:", e)
        return "https://via.placeholder.com/500x750?text=Error"


def recommend(movie):

    movie_index = movies[movies["title"] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    
    for item in movies_list:

        movie_id = movies.iloc[item[0]].movie_id
    

        recommended_movies.append(
            movies.iloc[item[0]].title
        )

        recommended_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_movies, recommended_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity  = pickle.load(open('similarity.pkl', 'rb'))


st.set_page_config(
    page_title="🎬 Movie Recommender",
    page_icon="🎥",
    layout="wide"
)

st.markdown(
    """
    <h1 style='text-align:center;color:#FF4B4B'>
        🎬 Movie Recommendation System
    </h1>
    """,
    unsafe_allow_html=True
) 

selected_movie_name = st.selectbox(
    "🎥 Select a Movie",
    movies["title"].values
)


if st.button("🎬 Recommend"):

    names, posters = recommend(selected_movie_name)

    st.markdown(
        "<h2 style='text-align:center;color:#E50914;'>Recommended For You</h2>",
        unsafe_allow_html=True
    )

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:

            st.image(posters[i], use_container_width=True)

            st.markdown(
                f"""
                <div style="
                    background-color:#202020;
                    border-radius:10px;
                    padding:10px;
                    text-align:center;
                    min-height:70px;
                ">
                    <b style="color:white;">{names[i]}</b>
                </div>
                """,
                unsafe_allow_html=True
            )






