# cinema-db
## A database for movies and some data


Access to over 18'000 movies from 1920 to 2023 with titles, runtimes, genres, casts, directors, posters, awards, ratings and even plots.
For most of the records you have access to budgets and box offices too.
Explore an even wider database with a list of more than 500 movies providers over 120 regions, giving you a combination of nearly 400'000 records to know anywhere you can watch the movie in your state.

The process gets the data, cleans it and stores it (ETL) in some .csv files, usable for other applications. 
You can start using the "MDb_Data_Collection_WebScraping" file to extract the first data made only by titles.
Then you'll need a few API Keys from OMDB and TMDB (you can find the links in the project) to get all the other data using the "MDb_Data_Collection_Api" file.

Use the MDb_Data_Casting to clean, cast and drop null data to obtain a new dataframe usable for Machine Learning or data anlysis.


In the future I'm going to add more files to obtain stats and some simple application to have fun with the dataframe. Collaborations and improvements are open and well accepted! 
