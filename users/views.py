from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from users.forms import UserForm, UserProfileForm, RegistrationForm, LoginForm
from django.contrib.auth.models import User
from social.models import FriendsList
from social.views import handle_add_friend, handle_delete_friend


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

	friend_ids = FriendsList.objects.values_list('friend_id', flat=True).filter(user=request.user)
	friend = FriendsList.objects.filter(user_id=request.user, friend_id=user_id).first()

	if request.method == 'POST':
		if 'add_friend' in request.POST:
			handle_add_friend(request, user_id)
		if 'delete_friend' in request.POST:
			handle_delete_friend(request, user_id)

		return redirect('profile', user_id=user_id)

	context = {'user_data': user_data,
	           'most_rated': most_rated,
	           'least_rated': least_rated,
	           'user_id': user_id,
	           'friend_ids': friend_ids,
	           'friend': friend}

	return render(request, 'users/profile.html', context)
