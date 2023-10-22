from abc import ABC, abstractmethod


class FriendsPresenterInterface(ABC):

    @abstractmethod
    def raise_request_already_sent_exception(self):
        pass

    @abstractmethod
    def raise_no_friend_request_exists_exception(self):
        pass

    @abstractmethod
    def raise_invalid_request_status(self):
        pass

    @abstractmethod
    def raise_max_friends_reached_exception(self):
        pass

    @abstractmethod
    def get_friends_response(self, friends_results_dto):
        pass

    @abstractmethod
    def get_pending_friends_requests(self, pending_request_result_dto):
        pass
