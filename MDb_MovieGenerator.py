import pandas as pd
import random

# This file is used by the API to execute various functions (for example to generate random movies for the users)

# Load data from CSV files
movies_providers = pd.read_csv('Movies_Providers.csv')
mdb = pd.read_csv('CLEAN 2023_Movies_DB.csv')
regions = pd.read_csv('Regions.csv')
# Default user state
user_state = 'US'
# Set the provider state by the user location
provider_state = movies_providers['State'] == user_state


def extract_movie(imdb_id):
        # Extract all the movie's data from the dataframe
        movie = mdb.loc[mdb['imdbID'] == imdb_id].iloc[0]
        title = movie['Title']
        genre = movie['Genre']
        runtime = movie['Runtime']                         
        plot =  movie['Plot']
        year = movie['Released']
        poster = movie['Poster']
        director = movie['Director']
        writer = movie['Writer']
        cast = movie['Actors']
        country = movie['Country']
        production = movie['Production']
        imdbRating = movie['imdbRating']
        imdbVotes = movie['imdbVotes']
        boxOffice = movie['BoxOffice']
        rottenTomatoesRating = movie['RottenTomatoesRating']
        metacriticRating = movie['MetacriticRating']
        budget = movie['Budget']  
        return(imdb_id, title, genre, runtime, plot, year, poster, 
                        director, writer, cast, country, production,
                        imdbRating, imdbVotes,boxOffice, rottenTomatoesRating,
                        metacriticRating, budget)


# Function to extract the watch options for a movie from a df
def extract_watch_options(df, id):
    movie = df[df['imdbID'] == id].iloc[0]
    flatrate = True if movie['Flatrate'] else False
    free = True if movie['Free'] else False
    rent = True if movie['Rent'] else False
    buy = True if movie['Buy'] else False
    link = movie['Link']   
    return flatrate, free, rent, buy, link
 
 
# Function to filter a df by the user's state 
def filter_by_state(df, state):  
    state = user_state
    filtered = df.query('State == @state')
    return filtered


# Function to filter a df by the available ids for the user's State
def filter_by_id(df1, df2):
    # Get unique imdbIDs from df2
    unique_ids = df2['imdbID'].unique()
    # Filter df1 keeping only the unique ids and merge the watch options from df2
    filtered = df1[df1['imdbID'].isin(unique_ids)]
    filtered = filtered.merge(df2[['imdbID', 'Free', 'Flatrate', 'Buy', 'Rent', 'Link']], on='imdbID', how='left') 
    return filtered

# Funtion to filter a df by genre and runtime for the user's State
def filter_by_params(gen, runtime):
    filtered = filter_by_id(mdb, filter_by_state(movies_providers, user_state))
    # Splitting the first genre from the list of genres
    filtered['First Genre'] = filtered['Genre'].str.split(',').str[0]
    # Filter the movies based on the first genre and runtime
    filtered = filtered[(filtered['First Genre'] == gen) & (filtered['Runtime'] <= runtime)].sample(n=1)
    return filtered


def return_genres():
    top_genres = pd.read_csv('top_15_genres.csv')
    return top_genres.to_dict()


def change_user_location(state):
    user_state = state
    return user_state

    
# Creation of the class Movie
class Movie():
    def __init__(self, imdb_id, title, genre, runtime, plot, year, poster, 
                 director, writer, cast, country, production,
                  imdbRating, imdbVotes,boxOffice, rottenTomatoesRating,
                    metacriticRating, budget, flatrate, free, rent, buy, link):
        
        self.imdb_id = imdb_id
        self.title = title
        self.genre = genre
        self.runtime = runtime
        self.plot = plot
        self.year = year
        self.poster = poster
        self.director = director
        self.writer = writer
        self.cast = cast
        self.country = country
        self.production = production
        self.imdbRating= imdbRating
        self.imdbVotes = imdbVotes
        self.boxOffice = boxOffice
        self.rottenTomatoesRating = rottenTomatoesRating
        self.metacriticRating = metacriticRating
        self.budget = budget
        self.flatrate = flatrate
        self.free = free
        self.rent = rent
        self.buy = buy
        self.link = link

    # Method to generate random a movie (.sample(n=1)) + available providers 
    # from a df of movies available for the user's state
    def generate_movie():
        filtered_movies = filter_by_id(mdb, filter_by_state(movies_providers,user_state)).sample(n=1)
        imdb_id = filtered_movies.iloc[0]['imdbID']
        movie_args = extract_movie(imdb_id)
        watch_options = extract_watch_options(filtered_movies, imdb_id)
        return Movie(*movie_args, *watch_options)
    
    
    # Method to obtain the movie info by its imdb_id
    def get_movie(imdb_id):        
        filtered_movies = filter_by_id(mdb, filter_by_state(movies_providers,user_state))
        movie_args = extract_movie(imdb_id)
        watch_options = extract_watch_options(filtered_movies, imdb_id)
        return Movie(*movie_args, *watch_options)        
    
    
    def filter_movies(gen, runtime):
        filtered_movies = filter_by_params(gen, runtime)
        # Extract the imdbID from the filtered DataFrame
        imdb_id = filtered_movies.iloc[0]['imdbID']
        movie_args = extract_movie(imdb_id)
        watch_options = extract_watch_options(filtered_movies, imdb_id)
        return Movie(*movie_args, *watch_options)  