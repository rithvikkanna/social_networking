from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from django.contrib.auth import authenticate, login
from friends.serializers.serializers import SearchQuerySerializer, UserLoginSerializer
from friends.interactors.search_users import SearchUsersInteractor
from friends.storages.user_storage import UserStorageImplementation
from friends.presenters.presenter_implementation import UserSignUpPresenterImplementation
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from friends.interactors.get_pending_friend_requests import GetPendingRequests
from friends.storages.friends_storage import FriendsStorage
from friends.presenters.friends_presenter_implementation import FriendsPresenterImplementation


@api_view(["GET"])
@authentication_classes([OAuth2Authentication])
def get_pending_requests(request):
    limit = request.GET.get('limit', 10)
    offset = request.GET.get('offset', 0)

    user_id = request.user.id
    storage = FriendsStorage()
    user_storage = UserStorageImplementation()
    presenter = FriendsPresenterImplementation()
    user_presenter = UserSignUpPresenterImplementation()
    interactor = GetPendingRequests(friends_storage=storage)

    response = interactor.get_pending_requests_wrapper(user_id=user_id, limit=limit, offset=offset,
                                                       friends_presenter=presenter,
                                                       user_presenter=user_presenter)
    return response
