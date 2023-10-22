from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from friends.serializers.serializers import UserSignupSerializer, UserLoginSerializer
from friends.interactors.user_login import UserLoginInteractor
from friends.storages.user_storage import UserStorageImplementation
from friends.presenters.presenter_implementation import UserSignUpPresenterImplementation
from common.oauth2_storage import OAuth2SQLStorage

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email_id = serializer.validated_data.get('email_id')
        password = serializer.validated_data.get('password')

        storage = UserStorageImplementation()
        oauth2_storage = OAuth2SQLStorage()
        presenter = UserSignUpPresenterImplementation()
        interactor = UserLoginInteractor(user_storage=storage, oauth2_storage=oauth2_storage)
        response = interactor.user_login_wrapper(email_id=email_id, password=password, user_presenter=presenter)
        return response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
