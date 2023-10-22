from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from friends.serializers.serializers import UserSignupSerializer, UserLoginSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSignupSerializer(data=request.data)
    if serializer.is_valid():
        email_id = serializer.validated_data.get('email_id')
        password = serializer.validated_data.get('password')
        name = serializer.validated_data.get('name')
        from friends.interactors.user_signup import UserSignup
        from friends.storages.user_storage import UserStorageImplementation
        from friends.presenters.presenter_implementation import UserSignUpPresenterImplementation
        storage = UserStorageImplementation()
        presenter = UserSignUpPresenterImplementation()
        interactor = UserSignup(user_storage=storage)
        response = interactor.user_signup_wrapper(name=name, email_id=email_id, password=password,
                                                  user_presenter=presenter)
        return response

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
