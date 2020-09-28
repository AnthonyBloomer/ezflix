from ezflix import Ezflix

ezflix = Ezflix(query="Goodfellas", media_type="movie", quality="720p", limit=1)
movies = ezflix.search()
for movie in movies:
    print(movie["link"])
