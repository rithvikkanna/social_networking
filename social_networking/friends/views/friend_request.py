from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from django.contrib.auth import authenticate, login
from friends.serializers.serializers import FriendRequestSerializer
from friends.interactors.search_users import SearchUsersInteractor
from friends.storages.user_storage import UserStorageImplementation
from friends.presenters.presenter_implementation import UserSignUpPresenterImplementation
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from friends.interactors.friend_request_interactor import FriendRequestInteractor
from friends.storages.friends_storage import FriendsStorage
from friends.presenters.friends_presenter_implementation import FriendsPresenterImplementation
from friends.interactors.dtos.friends_dtos import FriendRequestParamsDTO
from friends.presenters.presenter_implementation import UserSignUpPresenterImplementation


@api_view(["POST"])
@authentication_classes([OAuth2Authentication])
def friend_request(request):
    serializer = FriendRequestSerializer(data=request.data)
    if serializer.is_valid():
        action = serializer.validated_data.get('action')
        sender_user_id = serializer.validated_data.get('sender_user_id')
        receiver_user_id = serializer.validated_data.get('receiver_user_id')
        friend_request_params_dto = FriendRequestParamsDTO(
            action=action,
            sender_user_id=sender_user_id,
            receiver_user_id=receiver_user_id
        )
        friend_storage = FriendsStorage()
        user_storage = UserStorageImplementation()
        friends_presenter = FriendsPresenterImplementation()
        user_presenter = UserSignUpPresenterImplementation()
        interactor = FriendRequestInteractor(user_storage=user_storage, friends_storage=friend_storage)
        interactor.friend_request_wrapper(friend_request_params=friend_request_params_dto,
                                          friends_presenter=friends_presenter, user_presenter=user_presenter)

        return Response("Request Processed Successfully", status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
