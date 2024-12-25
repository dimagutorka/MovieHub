from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from users.forms import UserForm, UserProfileForm, RegistrationForm, LoginForm
from django.contrib.auth.models import User
from social.models import FriendsList
from social.forms import AddFriend


@login_required(login_url='/login/')
def update_user_profile_view(request):
	if request.method == 'POST':

		form_user = UserForm(request.POST, instance=request.user)
		form_userprofile = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)

		if form_user.is_valid() and form_userprofile.is_valid():
			form_user.save()
			form_userprofile.save()
			messages.success(request, 'Your profile has been updated')
			return redirect('home')

	else:
		form_user = UserForm(instance=request.user)
		form_userprofile = UserProfileForm(instance=request.user.profile)

	return render(request, 'users/profile_update.html', {
		'form_user': form_user,
		'form_userprofile': form_userprofile
	})


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
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			request.session['username'] = user.username
			return redirect('home')
	else:
		form = RegistrationForm()
	return render(request, 'users/registration.html', {'form': form})


@login_required(login_url='/login/')
def logout_view(request):
	logout(request)
	return redirect('home')


@login_required(login_url='/login/')
def user_profile_view(request, user_id):
	request_user_id = request.user
	user = User.objects.get(id=user_id)
	user_data = User.objects.select_related('profile').get(id=user_id)
	friend = FriendsList.objects.filter(user_id=request_user_id, friend_id=user_id).first()

	most_rated = user.rates.all().order_by('-rate')[:3]
	least_rated = user.rates.all().order_by('rate')[:3]

	friend_ids = FriendsList.objects.values_list('friend_id', flat=True).filter(user=request_user_id)

	if request.method == 'POST':

		if 'add_friend' in request.POST:
			user_fried_form = AddFriend(request.POST)
			if user_fried_form.is_valid():
				form = user_fried_form.save(commit=False)
				form.user = request_user_id
				form.friend = user
				form.save()

		if 'delete_friend' in request.POST:
			FriendsList.objects.get(friend_id=user_id).delete()

		return redirect('profile', user_id=user_id)

	context = {'user_data': user_data,
	           'most_rated': most_rated,
	           'least_rated': least_rated,
	           'user_id': user_id,
	           'friend_ids': friend_ids,
	           'friend': friend}

	return render(request, 'users/profile.html', context)
