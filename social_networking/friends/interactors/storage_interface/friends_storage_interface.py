from abc import ABC, abstractmethod
from friends.constants.enums import FriendRequestStatus
from datetime import datetime


class FriendStorageInterface(ABC):

    @abstractmethod
    def get_user_friends(self, user_id: str, limit: int, offset: int):
        pass

    @abstractmethod
    def get_user_pending_friend_requests(self, user_id, limit: int, offset: int):
        pass

    @abstractmethod
    def accept_friend_request(self, friend_request_accepted_user_id: str, friend_request_sent_user_id: str):
        pass

    @abstractmethod
    def send_friend_request(self, friend_request_received_user_id: str, friend_request_sent_user_id: str):
        pass

    @abstractmethod
    def reject_friend_request(self, friend_request_rejected_user_id: str, friend_request_sent_user_id: str):
        pass

    @abstractmethod
    def get_user_requests_by_status(self, friend_request_sent_user_id: str, friend_request_received_user_id: str,
                                    status: FriendRequestStatus):
        pass

    @abstractmethod
    def get_user_send_friend_request(self, user_id: str, requested_at: datetime):
        pass

    @abstractmethod
    def check_existing_user_request(self, sender_user_id: str, receiver_user_id: str):
        pass
