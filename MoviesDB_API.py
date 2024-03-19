from flask import Flask, jsonify, request
import MDb_MovieGenerator as mdb

app = Flask(__name__)

# Function to format the JSON repsonse
def create_movie_response(movie):
    return {
        'title': movie.title,
        'director': movie.director,
        'cast': movie.cast,
        'link': movie.link,
        'imdbid': movie.imdb_id,
        'genre': movie.genre,
        'runtime': movie.runtime,
        'plot': movie.plot,
        'year': movie.year,
        'writer': movie.writer,
        'country': movie.country,
        'production': movie.production,
        'poster': movie.poster,
        'flatrate': movie.flatrate,
        'free':  movie.free,
        'rent': movie.rent,
        'buy': movie.buy,
        'imdbRating': movie.imdbRating,
        'imdbVotes': movie.imdbVotes,
        'boxOffice': movie.boxOffice,
        'rottenTomatoesRating': movie.rottenTomatoesRating,
        'metacriticRating': movie.metacriticRating,
        'budget': movie.budget
    }


# Routes
##########

# Home
@app.route('/')
def index():
    return 'Movie_DB API' 

# Random Movie
@app.route('/api/random_movie/', methods=['GET'])
def get_random_movie():
    state = request.args.get('state')
    mdb.user_state = state
    movie = mdb.Movie.generate_movie()
    return jsonify(create_movie_response(movie))

# Get Movie By Id
@app.route('/api/get_movie/<imdb_id>/', methods=['GET'])   
def get_movie(imdb_id):
    state = request.args.get('state')
    mdb.user_state = state
    movie = mdb.Movie.get_movie(imdb_id)
    return jsonify({
        'title': movie.title,
        'director': movie.director,
        'cast': movie.cast,
        'link': movie.link,
        'imdbid': movie.imdb_id,
        'genre': movie.genre,
        'runtime': movie.runtime,
        'plot': movie.plot,
        'year': movie.year,
        'writer': movie.writer,
        'country': movie.country,
        'production': movie.production,
        'poster': movie.poster,
        'flatrate': movie.flatrate,
        'free':  movie.free,
        'rent': movie.rent,
        'buy': movie.buy
    })


# Filter Movies By Params
# example: /api/filter_movies/?gen=Comedy&runtime=90
@app.route('/api/filter_movies/', methods=['GET'])   
def filter_movies():
    state = request.args.get('state')
    mdb.user_state = state
    gen = request.args.get('gen')
    runtime = request.args.get('runtime')
    movie = mdb.Movie.filter_movies(gen, int(runtime))
    return jsonify(create_movie_response(movie))

# Get top genres
@app.route('/api/top_genres/', methods=['GET'])
def return_genres():
    genres = mdb.return_genres()
    return jsonify(genres)

    
# Quiz moive: guees the title based on
@app.route('/api/movie_quiz/', methods=['GET'])
def get_movie_quiz():
    movie = mdb.Movie.generate_movie()
    hints, options = movie.quiz_command()
    return jsonify({
        'hints': hints,
        'options': options
    })



if __name__ == '__main__':
    app.run(debug=True)
    
    
