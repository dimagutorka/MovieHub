from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import FriendRequest, FriendList, BlackList
from django.db.models import Q


def handle_send_friend_request(request, current_user, friend):
	FriendRequest.objects.create(from_user=current_user, to_user=friend)
	messages.success(request, 'Request to friends was sent successfully')


def handle_withdraw_friend_request(request, current_user, friend):
	FriendRequest.objects.get(from_user=current_user, to_user=friend).delete()


def handle_delete_friend(request, is_friends):
	is_friends.delete()


def handle_accept_friend(request, friend, current_user):
	FriendList.objects.create(user1=current_user, user2=friend)
	FriendRequest.objects.get(from_user=friend, to_user=current_user).delete()
	messages.success(request, 'Friend accepted')


def handle_decline_friend(request, friend, current_user):
	FriendRequest.objects.get(from_user=friend, to_user=current_user).delete()
	messages.info(request, "Friend request declined.")


@login_required(login_url='/login/')
def friends_list_view(request):
	friendship = (FriendList.objects.filter(Q(user1=request.user.id) | Q(user2=request.user.id)))
	friends_list = [friend.user1_id if friend.user2_id == request.user.id else friend.user2_id for friend in friendship]
	current_list_of_friends = User.objects.filter(pk__in=friends_list)

	pending_requests_to_friends = (FriendRequest.objects.values_list('from_user', flat=True).filter(to_user=request.user.id))
	pending_users_to_friends = User.objects.filter(pk__in=pending_requests_to_friends)

	if request.method == 'POST':
		friend_id = request.POST.get('friend_request_id', None)
		current_user = User.objects.get(pk=request.user.id)

		if "accept_friend" in request.POST:
			friend = User.objects.get(pk=friend_id)
			handle_accept_friend(request, friend, current_user)

		elif "decline_friend" in request.POST:
			friend = User.objects.get(pk=friend_id)
			handle_decline_friend(request, friend, current_user)

		elif 'delete_friend' in request.POST:
			current_friend_id = request.POST.get('current_friend_id', None)
			is_friends = (FriendList.objects.filter(
				Q(user1=request.user.id, user2=current_friend_id) |
				Q(user1=current_friend_id, user2=request.user.id))).first()

			handle_delete_friend(request, is_friends)

		return redirect('friends')

	return render(request, 'socials/friends.html',
	              {'friends_list': friends_list,
	               'pending_friends': pending_users_to_friends,
	               'current_list_of_friends': current_list_of_friends})
