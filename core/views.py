from django.db.models import Avg, Count
from django.shortcuts import render
from movies.models import Movies


# TODO-20: Movies status - to watch / watching / watched / on hold / backlog
# TODO-9: Make users' profiles which post comments active Other users can click on their avatar/nickname and go to their profile
# TODO-7: Add validation in forms form unathorized user who click rate/watch latter buttons
# TODO-6: add field avatar + last_updated/created to comment section on a movie page
# TODO-5: Refactor views (too long)
# TODO-4: Add movies you can like (think about ideas how it could be implemented)
# TODO-15: There's an error when anon user try to post comments or open page with rate thingy
# TODO-10: ПОПРОБОВАТЬ ПЕРЕСВЯЗАТЬ ВСЕ ЧЕРЕЗ ТАБЛИЦУ ЮЗЕРОВ usr = User.objects.get(id=1) | usr.friends

def some_filters(request):
	num_comments = Movies.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')
	avg_rating = Movies.objects.annotate(avg_rating=Avg('rates', default=1)).order_by('-avg_rating')

	contex = {'num_comments': num_comments, 'avg_rating': avg_rating}

	return render(request, 'home.html', contex)


def home(request):
	username = request.session['username'] if 'username' in request.session else 'Guest'

	movies = Movies.objects.all()
	the_most_discussed_movies = movies.annotate(num_comments=Count('comments')).order_by('-num_comments')[:5]
	the_most_rated_movies = movies.order_by('-average_rating')[:5]
	recently_released = movies.order_by('-release_date')[:5]

	return render(request, 'home.html', {
		'username': username,
		'the_most_discussed_movies': the_most_discussed_movies,
		'most_rated_movies': the_most_rated_movies,
		'recently_released': recently_released})
