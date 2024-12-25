from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Count, Avg
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddToWatchLater, MovieForm
from .models import Genres, Movies
from core.forms import CommentForm, RateForm
from core.models import Rate


def handle_comment_submission(request, movie):
	comment_form = CommentForm(request.POST)

	if comment_form.is_valid():
		comment = comment_form.save(commit=False)
		comment.user = request.user
		comment.movie = movie
		comment.save()
		messages.success(request, message='Your comment has been added')
	return comment_form


def handle_rate_submission(request, movie):
	rate_form = RateForm(request.POST)

	if rate_form.is_valid():
		rate = rate_form.save(commit=False)
		rate.user = request.user
		rate.movie = movie
		rate.save()
		messages.success(request, message='Your rate has been added')
	return rate_form


def handle_watch_later_list(request, movie):
	watch_later_form = AddToWatchLater(request.POST)

	if watch_later_form.is_valid():
		form = watch_later_form.save(commit=False)
		form.user = request.user
		form.movie = movie
		form.save()
	return watch_later_form


@login_required(login_url='/login/')
def create_movie_view(request):
	form = MovieForm()
	if request.method == 'POST':
		form = MovieForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'Your movie has been created')
			return redirect('home')
	else:
		return render(request, 'movies/movie_create.html', {"form": form})


def genres_list_view(request):
	all_genres = Genres.objects.prefetch_related('movies')
	num_comments = (Movies.objects.prefetch_related('genres')
	                .annotate(num_comments=Count('comments')).order_by('-num_comments'))

	return render(request, 'movies/genres_list.html',
	              {'genres': all_genres, 'num_comments': num_comments})


def genre_detail_view(request, genre_id):
	genre = get_object_or_404(Genres, pk=genre_id)
	all_movies_in_genre = genre.movies.values('id', 'title')
	context = {'movies': all_movies_in_genre}

	return render(request, 'movies/genre_detail.html', context)


def update_recently_visited_view(request, movie_id):
	recently_viewed = request.session.get("recently_viewed", [])

	if movie_id in recently_viewed:
		recently_viewed.remove(movie_id)
		recently_viewed.insert(0, movie_id)

	elif movie_id not in recently_viewed:
		recently_viewed.insert(0, movie_id)

	if len(recently_viewed) > 5:
		recently_viewed.pop()

	request.session["recently_viewed"] = recently_viewed
	request.session.modified = True

	return Movies.objects.filter(id__in=recently_viewed)


def movie_detail_view(request, movie_id):
	movie = get_object_or_404(Movies, pk=movie_id)
	avg_movie_rate = movie.rates.all().aggregate(Avg('rate'))['rate__avg']
	genres_in_movie = movie.genres.all()
	comments = movie.comments.select_related('user').all()

	if request.user.is_authenticated:
		rate_instance = Rate.objects.filter(user=request.user, movie=movie).first()
		rate_form = RateForm(instance=rate_instance)
	else:
		rate_form = RateForm()

	# Empty forms
	watch_later_form = AddToWatchLater()
	comment_form = CommentForm()

	if request.method == 'POST':
		if 'comment_submit' in request.POST:
			comment_form = handle_comment_submission(request, movie)
			return redirect('movie', movie_id=movie_id)

		elif 'rate_submit' in request.POST and request.user.is_authenticated:
			rate_form = handle_rate_submission(request, movie)
			return redirect('movie', movie_id=movie_id)

		# if movies + user exists else:
		elif 'watch_later_submit' in request.POST:
			watch_later_form = handle_watch_later_list(request, movie)
			return redirect('movie', movie_id=movie_id)

	recently_viewed_movies = update_recently_visited_view(request, movie_id)

	context = {
		'movie': movie,
		'comments': comments,
		'avg_movie_rate': avg_movie_rate,
		'comment_form': comment_form,
		'rate_form': rate_form,
		"recently_viewed": recently_viewed_movies,
		"genres_in_movie": genres_in_movie,
		"watch_later_form": watch_later_form,
	}

	return render(request, 'movies/movie_detail.html', context)


# @login_required(login_url='/login_page/')
# def import_movies_view(request):
# 	if request.method == 'POST':
# 		form = CSVFileForm(request.POST, request.FILES)
# 		context = {"form": form}
#
# 		if form.is_valid():
# 			csv_file_instance = form.save()
# 			messages.success(request, 'Your movie has been created')
#
# 			filename = csv_file_instance.csv_filename.name
# 			result = from_csvfile_to_bd.delay(filename)
#
# 			context['task_id'] = result.task_id
# 	# return redirect('home')
# 	else:
# 		form = CSVFileForm()
# 		context = {"form": form}
# 	return render(request, 'basic_site/movie_creation_via_csv.html', context)
