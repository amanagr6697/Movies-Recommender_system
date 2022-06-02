import pickle
import streamlit as st
import requests
import pandas as pd
#Mine API key: 841c6aac551d88c95627b74a672331f6

def fetch_image(movie_id):
    api_url = 'https://api.themoviedb.org/3/movie/{}?api_key=841c6aac551d88c95627b74a672331f6&language=en-US'.format(movie_id)
    
    #Taking requests and adding it to 
    data_value = requests.get(api_url)
    data_value = data_value.json()
    
    #Get the poster path from tmdb site 
    image_path = data_value['poster_path']
    
    #Gives complete image path to display
    full_path = "https://image.tmdb.org/t/p/w500/" + image_path
    
    return full_path



#To recommend movies based on a particular movie
def recommend_movies(movie):
    
    #Get the index of the movie from the data set to calculate similarity and poster
    index = movies[movies['title'] == movie].index[0]
    
    #Get similarity values corresponding to that movie w.r.t to another movies
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    #Movie names and poster array
    recommended_movie_names = []
    corresponding_posters = []
    
    #Iterate over first 6 movies obviously leaving the 0th 1 as that is that movie only.
    for i in distances[1:7]:
        
        #Taking the movie_id to capture poster
        movie_id = movies.iloc[i[0]].movie_id
        
        #Generating poster and pushing in the poster array
        corresponding_posters.append(fetch_image(movie_id))
        
        #Getting title of the movie and pushing in the names array
        recommended_movie_names.append(movies.iloc[i[0]].title)
    
    #Returning values
    return recommended_movie_names,corresponding_posters

#Defining header
st.header('Similar Movies Recommender System')

#Getting info from pickle file to get movie id and similarity.
movies = pickle.load(open('movie_list.pkl','rb'))
movies=pd.DataFrame(movies)
similarity = pickle.load(open('similarity.pkl','rb'))

#Displaying all movies as a drop-down list.
movie_list = movies['title'].values

#Button to show recommendations.
selected_movie = st.selectbox(
    "TYPE OR SELECT YOUR FAVOURITE MOVIE",
    movie_list
)

#If button clicked
if st.button('GIVE RECOMMENDATIONS'):
    st.header("Here are your recommendations: ")

    #Calling function to get movie names and posters
    recommended_movie_names,corresponding_posters = recommend_movies(selected_movie)
    
    #Displaying movie name and poster in 6 columns
    column_1, column_2, column_3, column_4,column_5,column_6 = st.columns(6)
    with column_1:
        st.text(recommended_movie_names[0])
        st.image(corresponding_posters[0])
    
    with column_2:
        st.text(recommended_movie_names[1])
        st.image(corresponding_posters[1])
    
    with column_3:
        st.text(recommended_movie_names[2])
        st.image(corresponding_posters[2])
   
    with column_4:
        st.text(recommended_movie_names[3])
        st.image(corresponding_posters[3])
    
    with column_5:
        st.text(recommended_movie_names[4])
        st.image(corresponding_posters[4])
    
    with column_6:
        st.text(recommended_movie_names[5])
        st.image(corresponding_posters[5])




