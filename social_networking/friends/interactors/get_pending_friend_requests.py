from friends.interactors.storage_interface.friends_storage_interface import FriendStorageInterface
from friends.exceptions.exceptions import InvalidLimitValue, InvalidOffsetValue, InvalidUserID
from friends.interactors.presenter_interface.user_presenter_interface import UserPresenterInterface
from friends.interactors.presenter_interface.friends_presenter_interface import FriendsPresenterInterface
from friends.interactors.mixins.validation_mixin import ValidationMixin


class GetPendingRequests(ValidationMixin):
    def __init__(self, friends_storage: FriendStorageInterface):
        self.friends_storage = friends_storage

    def get_pending_requests_wrapper(self, user_id: str, limit: int, offset: int,
                                     friends_presenter: FriendsPresenterInterface,
                                     user_presenter: UserPresenterInterface
                                     ):

        try:

            pending_request_dto = self.get_pending_requests(user_id=user_id, limit=limit, offset=offset)
            response = friends_presenter.get_pending_friends_requests(pending_request_result_dto=pending_request_dto)
            return response
        except InvalidLimitValue:
            response = user_presenter.raise_invalid_limit_error()
            return response
        except InvalidOffsetValue:
            response = user_presenter.raise_invalid_user_id_exception()
            return response

    def get_pending_requests(self, user_id: str, limit: int, offset: int):
        self._validate_data(limit=limit, offset=offset)

        pending_requests = self.friends_storage.get_user_pending_friend_requests(user_id, limit=limit, offset=offset)
        return pending_requests

    def _validate_data(self, limit: int, offset: int):

        self.validate_limit_value(limit=limit)
        self.validate_offset_value(offset=offset)
