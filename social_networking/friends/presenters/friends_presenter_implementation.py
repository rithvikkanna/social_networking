import json
from django.http import response

from friends.interactors.presenter_interface.friends_presenter_interface import FriendsPresenterInterface
from friends.constants.constants import REQUEST_ALREADY_SENT, MAX_FRIENDS_REACHED, INVALID_REQUEST_STATUS, \
    NO_FRIEND_REQUEST_EXISTS


class FriendsPresenterImplementation(FriendsPresenterInterface):
    def raise_request_already_sent_exception(self):
        request_already_sent_dict = {
            "response": REQUEST_ALREADY_SENT[0],
            "http_status_code": 400,
            "res_status": REQUEST_ALREADY_SENT[1]
        }
        data = json.dumps(request_already_sent_dict)
        responses = response.HttpResponse(data, status=400)
        return responses

    def raise_no_friend_request_exists_exception(self):
        no_friend_request_exists_dict = {
            "response": NO_FRIEND_REQUEST_EXISTS[0],
            "http_status_code": 400,
            "res_status": NO_FRIEND_REQUEST_EXISTS[1]
        }
        data = json.dumps(no_friend_request_exists_dict)
        responses = response.HttpResponse(data, status=400)
        return responses

    def raise_invalid_request_status(self):
        invalid_request_status_dict = {
            "response": INVALID_REQUEST_STATUS[0],
            "http_status_code": 400,
            "res_status": INVALID_REQUEST_STATUS[1]
        }
        data = json.dumps(invalid_request_status_dict)
        responses = response.HttpResponse(data, status=400)
        return responses

    def raise_max_friends_reached_exception(self):
        max_friends_reached_dict = {
            "response": MAX_FRIENDS_REACHED[0],
            "http_status_code": 400,
            "res_status": MAX_FRIENDS_REACHED[1]
        }
        data = json.dumps(max_friends_reached_dict)
        responses = response.HttpResponse(data, status=400)
        return responses

    def get_friends_response(self, friends_results_dto):
        friends_result_dict = dict()
        friends_result_dict['total_count'] = friends_results_dto.total_count
        friends = friends_results_dto.friend_requests
        friends_list = self._get_friends_dict_list(friends=friends)
        friends_result_dict['friends'] = friends_list
        data = json.dumps(friends_result_dict)
        responses = response.HttpResponse(data, status=200)
        return responses

    @staticmethod
    def _get_friends_dict_list(friends):
        friends_list = []
        for friend in friends:
            friend_dict = dict()
            friend_dict['name'] = friend.name
            friend_dict['user_id'] = str(friend.user_id)
            friend_dict['email_id'] = friend.email_id
            friend_dict['is_admin'] = friend.is_admin
            friends_list.append(friend_dict)
        return friends_list

    def get_pending_friends_requests(self, pending_request_result_dto):
        friends_result_dict = dict()
        friends_result_dict['total_count'] = pending_request_result_dto.total_count
        friends = pending_request_result_dto.pending_requests
        friends_list = self._get_friends_dict_list(friends=friends)
        friends_result_dict['friends'] = friends_list
        data = json.dumps(friends_result_dict)
        responses = response.HttpResponse(data, status=200)
        return responses
