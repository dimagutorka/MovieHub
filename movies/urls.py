from django.urls import path
from movies.views import genres_list_view, genre_detail_view, movie_detail_view, create_movie_view


urlpatterns = [
	path('genres/', genres_list_view, name='genres'),
	path('genre/<int:genre_id>/', genre_detail_view, name='genre'),
	path('movie/<int:movie_id>', movie_detail_view, name='movie'),
	path('movie/create/', create_movie_view, name='movie_create'),
	# path('movies/import/', import_movies_view, name='movie_import'),

]

