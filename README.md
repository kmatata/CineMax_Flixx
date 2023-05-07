# CineMax_Flixx
The program is a generally of a movie ranking platform "Cinemania" and performs various operations related to movies. It uses Django, Django-ninja, and MongoDB for database management. The program includes the following functionalities:

1. Creation of a movie: When a POST request is made to "/movies", the program creates a new movie entry based on the provided data. If the movie's status is "coming-up", it assigns a random ranking between 0 and 5. Otherwise, it sets the ranking to 50. The movie details are stored in both the Django database and MongoDB.

2. Retrieval of movies: A GET request to "/movies" returns a list of all movies with their respective details from the Django database.

3. Deletion of a movie: A DELETE request to "/movies/{id}" deletes a movie with the specified ID from both the Django database and MongoDB.

4. Retrieval of trending movies: A GET request to "/trending_movies" fetches all movies from MongoDB that have a status of "running". The movies are sorted in descending order based on their ranking.

The program utilizes various modules and libraries such as datetime, pymongo, Django, Celery, pydantic, and more to handle data manipulation, serialization, and API endpoints.

Running:
