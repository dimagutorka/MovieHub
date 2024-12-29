from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from social.models import FriendRequest
from users.forms import UserForm, UserProfileForm, RegistrationForm, LoginForm
from django.contrib.auth.models import User
# from social.views import handle_add_friend, handle_delete_friend
from django.db.models import Q


@login_required(login_url='/login/')
def update_user_profile_view(request):
	form_user = UserForm(instance=request.user)
	form_userprofile = UserProfileForm(instance=request.user.profile)

	if request.method == 'POST':
		form_user = UserForm(request.POST, instance=request.user)
		form_userprofile = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)

		if form_user.is_valid() and form_userprofile.is_valid():
			form_user.save()
			form_userprofile.save()
			messages.success(request, 'Your profile has been updated')
			return redirect('home')

	return render(request, 'users/profile_update.html', {
		'form_user': form_user,
		'form_userprofile': form_userprofile})


def login_view(request):
	form = LoginForm(request.POST or None)
	if request.method == 'POST':
		username = request.POST.get('username', None)
		password = request.POST.get('password', None)
		user = authenticate(request, username=username, password=password)

		if user is not None:
			request.session.flush()
			login(request, user)
			messages.success(request, f'Welcome back, {user.username}!')
			return redirect('home')
		else:
			messages.error(request, 'Invalid username or password.')
			return redirect('login')

	return render(request, 'users/login.html', {"form": form})


def registration_view(request):
	form = RegistrationForm()

	if request.method == 'POST':
		form = RegistrationForm(request.POST)

		if form.is_valid():
			user = form.save()
			login(request, user)
			request.session['username'] = user.username
			return redirect('home')

	return render(request, 'users/registration.html', {'form': form})


@login_required(login_url='/login/')
def logout_view(request):
	logout(request)
	return redirect('home')


@login_required(login_url='/login/')
def user_profile_view(request, user_id):
	user = User.objects.get(id=user_id)
	user_data = User.objects.select_related('profile').get(id=user_id)

	most_rated = user.rates.all().order_by('-rate')[:3]
	least_rated = user.rates.all().order_by('rate')[:3]

	is_friend_relation_exists = (FriendRequest.objects.filter(
		Q(from_user=request.user.id, to_user=user_id) |
		Q(from_user=user_id, to_user=request.user.id))).first()

	if request.method == 'POST':
		if 'send_friend_request' in request.POST:
			if not is_friend_relation_exists:
				pass
			# handle_add_friend(request, user_id)

		if 'delete_friend' in request.POST:
			if is_friend_relation_exists and is_friend_relation_exists.status == 'accepted':
				pass  # handle_delete_friend(request, user_id)

		if 'withdraw_friend_request':
			if is_friend_relation_exists.status == 'pending':
				pass
			#  handle_withdraw_friend_request(request, user_id)

		return redirect('profile', user_id=user_id)

	context = {'user_data': user_data,
	           'most_rated': most_rated,
	           'least_rated': least_rated,
	           'user_id': user_id,
	           'friend_relation': is_friend_relation_exists}

	return render(request, 'users/profile.html', context)
