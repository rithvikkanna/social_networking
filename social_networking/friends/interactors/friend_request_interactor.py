from friends.interactors.storage_interface.friends_storage_interface import FriendStorageInterface
from friends.interactors.presenter_interface.friends_presenter_interface import FriendsPresenterInterface
from friends.interactors.storage_interface.user_storage_interface import UserStorageInterface
from friends.interactors.dtos.friends_dtos import FriendRequestParamsDTO
from friends.interactors.presenter_interface.user_presenter_interface import UserPresenterInterface
from friends.interactors.mixins.validation_mixin import ValidationMixin
from friends.exceptions.exceptions import InvalidUserID
from friends.constants.enums import FriendRequestStatus, FriendRequestAction
from friends.exceptions.exceptions import RequestAlreadySent, MaxFriendRequestReached, NoFriendRequestExits
from datetime import datetime, timedelta


class FriendRequestInteractor(ValidationMixin):
    def __init__(self, friends_storage: FriendStorageInterface, user_storage: UserStorageInterface):
        self.friends_storage = friends_storage
        self.user_storage = user_storage

    def friend_request_wrapper(self, friend_request_params: FriendRequestParamsDTO,
                               friends_presenter: FriendsPresenterInterface, user_presenter: UserPresenterInterface):

        try:
            self.friend_request(friend_request_params=friend_request_params)
        except InvalidUserID:
            response = user_presenter.raise_invalid_user_id_exception()
            return response
        except RequestAlreadySent:
            response = friends_presenter.raise_request_already_sent_exception()
        except MaxFriendRequestReached:
            response = friends_presenter.raise_max_friends_reached_exception()
            return response
        except NoFriendRequestExits:
            response = friends_presenter.raise_no_friend_request_exists_exception()
            return response

    def friend_request(self, friend_request_params: FriendRequestParamsDTO):
        self._validation(friend_request_params=friend_request_params)
        if friend_request_params.action == FriendRequestAction.SEND_REQUEST.value:
            self.send_friend_request_implementation(friend_request_params=friend_request_params)
        elif friend_request_params.action == FriendRequestAction.ACCEPT_REQUEST.value:
            self.accept_friend_request_implementation(friend_request_params=friend_request_params)
        elif friend_request_params.action == FriendRequestAction.REJECT_REQUEST.value:
            self.reject_friend_request_implementation(friend_request_params=friend_request_params)

    def _validation(self, friend_request_params: FriendRequestParamsDTO):
        requested_user_ids = [friend_request_params.receiver_user_id, friend_request_params.sender_user_id]
        self.validate_user_ids(user_ids=requested_user_ids, user_storage=self.user_storage)

    def send_friend_request_implementation(self, friend_request_params: FriendRequestParamsDTO):
        is_existing_requests_present = self.friends_storage.check_existing_user_request(
            sender_user_id=friend_request_params.sender_user_id,
            receiver_user_id=friend_request_params.receiver_user_id)
        if is_existing_requests_present:
            raise RequestAlreadySent
        one_minute_ago = datetime.now() - timedelta(minutes=1)
        user_sent_requests_last_one_min = self.friends_storage.get_user_send_friend_request(
            user_id=friend_request_params.sender_user_id, requested_at=one_minute_ago)
        if len(user_sent_requests_last_one_min) >= 3:
            raise MaxFriendRequestReached
        self.friends_storage.send_friend_request(friend_request_sent_user_id=friend_request_params.sender_user_id,
                                                 friend_request_received_user_id=friend_request_params.receiver_user_id)
        return

    def accept_friend_request_implementation(self, friend_request_params: FriendRequestParamsDTO):
        check_friend_request_already_sent = self.friends_storage.get_user_requests_by_status(
            friend_request_sent_user_id=friend_request_params.sender_user_id,
            friend_request_received_user_id=friend_request_params.receiver_user_id,
            status=FriendRequestStatus.PENDING.value)
        if not check_friend_request_already_sent:
            raise NoFriendRequestExits
        self.friends_storage.accept_friend_request(friend_request_sent_user_id=friend_request_params.sender_user_id,
                                                   friend_request_accepted_user_id=friend_request_params.receiver_user_id)
        return

    def reject_friend_request_implementation(self, friend_request_params: FriendRequestParamsDTO):
        check_friend_request_already_sent = self.friends_storage.get_user_requests_by_status(
            friend_request_sent_user_id=friend_request_params.sender_user_id,
            friend_request_received_user_id=friend_request_params.receiver_user_id,
            status=FriendRequestStatus.PENDING.value)
        if not check_friend_request_already_sent:
            raise NoFriendRequestExits
        self.friends_storage.reject_friend_request(friend_request_sent_user_id=friend_request_params.sender_user_id,
                                                   friend_request_rejected_user_id=friend_request_params.receiver_user_id)

