from friends.interactors.storage_interface.friends_storage_interface import FriendStorageInterface
from friends.interactors.storage_interface.user_storage_interface import UserStorageInterface
from friends.interactors.presenter_interface.friends_presenter_interface import FriendsPresenterInterface
from friends.interactors.mixins.validation_mixin import ValidationMixin
from friends.exceptions.exceptions import InvalidLimitValue, InvalidOffsetValue, InvalidUserID
from friends.interactors.presenter_interface.user_presenter_interface import UserPresenterInterface


class GetFriendsInteractor(ValidationMixin):
    def __init__(self, friends_storage: FriendStorageInterface):

        self.friends_storage = friends_storage

    def get_friends_wrapper(self, user_id: str, friends_presenter: FriendsPresenterInterface, limit: int, offset: int,
                            user_presenter: UserPresenterInterface):

        try:
            friends_result_dto = self.get_friends(user_id=user_id, limit=limit, offset=offset)
            response = friends_presenter.get_friends_response(friends_results_dto=friends_result_dto)
            return response

        except InvalidLimitValue:
            response = user_presenter.raise_invalid_limit_error()
            return response
        except InvalidOffsetValue:
            response = user_presenter.raise_invalid_offset_error()
            return response

        except InvalidUserID:
            response = user_presenter.raise_invalid_user_id_exception()
            return response

    def get_friends(self, user_id: str, limit: int, offset: int):

        self._validate_data(user_id=user_id, limit=limit, offset=offset)
        friends_result_dto = self.friends_storage.get_user_friends(user_id=user_id, limit=limit, offset=offset)
        return friends_result_dto

    def _validate_data(self, user_id: str, limit: int, offset: int):

        self.validate_limit_value(limit=limit)
        self.validate_offset_value(offset=offset)
