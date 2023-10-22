import re

from friends.interactors.storage_interface.user_storage_interface import UserStorageInterface
from friends.interactors.presenter_interface.user_presenter_interface import UserPresenterInterface
from friends.constants.config import EMAIL_REGEX_VALIDATION, PASSWORD_REGEX_VALIDATION
from friends.exceptions.exceptions import InvalidCredentials, InvalidEmailID
from common.oauth2_storage import OAuth2SQLStorage
from common.oauth_user_auth_tokens_service import OAuthUserAuthTokensService
from friends.interactors.dtos.user_dtos import UserAuthDTO


class UserLoginInteractor:
    def __init__(self, user_storage: UserStorageInterface, oauth2_storage: OAuth2SQLStorage):
        self.user_storage = user_storage
        self.oauth2_storage = oauth2_storage


    def user_login_wrapper(self, email_id: str, password: str, user_presenter: UserPresenterInterface):
        try:

            access_token_dto = self.user_login(email_id=email_id, password=password)
            response = user_presenter.get_access_token_response(access_token_dto=access_token_dto)
            return response
        except InvalidEmailID:
            response = user_presenter.raise_invalid_email_id_exception()
            return response
        except InvalidCredentials:
            response = user_presenter.raise_invalid_credentials()
            return response

    def user_login(self, email_id: str, password: str):
        if not re.match(EMAIL_REGEX_VALIDATION, email_id.lower()):
            raise InvalidEmailID
        user_dtos = self.user_storage.validate_email_id(email_id=email_id)
        if not user_dtos:
            raise InvalidCredentials
        is_valid_password = self.user_storage.validate_user_password(email_id=email_id, password=password)

        if not is_valid_password:
            raise InvalidCredentials

        service_obj = OAuthUserAuthTokensService(
            oauth2_storage=self.oauth2_storage
        )
        user_oath_dto = service_obj.create_user_auth_tokens(user_id=user_dtos[0].user_id)
        user_oath_dto_with_is_admin_status = UserAuthDTO(
            user_id=user_oath_dto.user_id,
            access_token=user_oath_dto.access_token,
            refresh_token=user_oath_dto.refresh_token,
            expires_in=user_oath_dto.expires_in
        )

        return user_oath_dto_with_is_admin_status

