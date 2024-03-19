# cinema-db
## A database for movies and some data


Access to over 18'000 movies from 1920 to 2023 with titles, runtimes, genres, casts, directors, posters, awards, ratings and even plots.
For most of the records you have access to budgets and box offices too.
Explore an even wider database with a list of more than 500 movies providers over 120 regions, giving you a combination of nearly 400'000 records to know anywhere you can watch the movie in your state.

# ETL process to create your own movies DataBase 

The process gets the data, cleans it and stores it (ETL) in some .csv files, usable for other applications. 
You can start using the "MDb_Data_Collection_WebScraping" file to extract the first data made only by titles.
Then you'll need a few API Keys from OMDB and TMDB (you can find the links in the project) to get all the other data using the "MDb_Data_Collection_Api" file.
Use the MDb_Data_Casting to clean, cast and drop null data to obtain a new dataframe usable for Machine Learning or data anlysis.


# Movie module + API application

The MoviesDB_API.py gives you an easy and clean access to the MDb_MovieGenerator.py with some built-in functions like a movie suggestor based on some inputs parameters and user's provider location.

# MDB TELEGRAM BOT 🤖🤖

A brand new telegram bot to have fun with the Movies database that uses direct GET calls to the API.
