from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from django.contrib.auth import authenticate, login
from friends.serializers.serializers import SearchQuerySerializer, UserLoginSerializer
from friends.interactors.search_users import SearchUsersInteractor
from friends.storages.user_storage import UserStorageImplementation
from friends.presenters.presenter_implementation import UserSignUpPresenterImplementation
from oauth2_provider.contrib.rest_framework import OAuth2Authentication


@api_view(["GET"])
@authentication_classes([OAuth2Authentication])
def search_users(request):

    input_serializer = SearchQuerySerializer(data=request.GET)

    if input_serializer.is_valid():
        # Valid input parameters
        search_key = input_serializer.validated_data['search_key']
        limit = input_serializer.validated_data.get('limit', 10)
        offset = input_serializer.validated_data.get('offset', 0)

        storage = UserStorageImplementation()
        presenter = UserSignUpPresenterImplementation()

        interactor = SearchUsersInteractor(user_storage=storage)
        response = interactor.search_users_wrapper(
            search_query=search_key, limit=limit, offset=offset, user_presenter=presenter)
        return response
    return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

