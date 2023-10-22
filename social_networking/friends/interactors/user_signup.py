import re

from friends.interactors.storage_interface.user_storage_interface import UserStorageInterface
from friends.interactors.presenter_interface.user_presenter_interface import UserPresenterInterface
from friends.constants.config import EMAIL_REGEX_VALIDATION, PASSWORD_REGEX_VALIDATION
from friends.exceptions.exceptions import UserAlreadyExists, InvalidEmailID, WeekPassword


class UserSignup:
    def __init__(self, user_storage: UserStorageInterface):
        self.user_storage = user_storage

    def user_signup_wrapper(self, name: str, email_id: str, password: str, user_presenter: UserPresenterInterface):

        try:
            user_dto = self.user_sign_up(email_id=email_id, name=name, password=password)
            return user_presenter.created_user_id_response(user_id=user_dto.user_id)
        except UserAlreadyExists:
            response = user_presenter.raise_user_already_exists_exception()
            return response
        except InvalidEmailID:
            response = user_presenter.raise_invalid_email_id_exception()
            return response
        except WeekPassword:
            response = user_presenter.raise_invalid_password_exception()
            return response

    def user_sign_up(self, name: str, email_id: str, password: str):

        if not re.match(EMAIL_REGEX_VALIDATION, email_id.lower()):
            raise InvalidEmailID
        if not re.match(PASSWORD_REGEX_VALIDATION, password):
            raise WeekPassword
        user_dtos = self.user_storage.validate_email_id(email_id=email_id)

        if user_dtos:
            raise UserAlreadyExists

        user_dto = self.user_storage.create_user(email_id=email_id, password=password, name=name)

        return user_dto
