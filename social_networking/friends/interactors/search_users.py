from friends.interactors.storage_interface.user_storage_interface import UserStorageInterface
from friends.interactors.presenter_interface.user_presenter_interface import UserPresenterInterface
from friends.constants.config import EMAIL_REGEX_VALIDATION, PASSWORD_REGEX_VALIDATION
from friends.exceptions.exceptions import InvalidLimitValue, InvalidOffsetValue


class SearchUsersInteractor:
    def __init__(self, user_storage: UserStorageInterface):
        self.user_storage = user_storage

    def search_users_wrapper(self, search_query: str, limit: int, offset: int, user_presenter: UserPresenterInterface):
        try:
            search_dtos = self.search_users(search_query=search_query, limit=limit, offset=offset)
            response = user_presenter.get_all_users_response(search_users_result_dtp=search_dtos)
            return response
        except InvalidLimitValue:
            error_response = user_presenter.raise_invalid_limit_error()
            return error_response
        except InvalidOffsetValue:
            error_response = user_presenter.raise_invalid_offset_error()
            return error_response

    def search_users(self, search_query: str, limit: int, offset: int):

        self._validate_query_parameters(limit=limit, offset=offset)

        user_dtos = self.user_storage.get_users_by_name(search_query=search_query, limit=limit, offset=offset)

        return user_dtos

    @staticmethod
    def _validate_query_parameters(limit: int, offset: int):
        if limit < 1:
            raise InvalidLimitValue
        if offset < 0:
            raise InvalidOffsetValue
