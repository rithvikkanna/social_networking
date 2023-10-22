from friends.constants.constants import (
    INVALID_EMAIL_ID, INVALID_PASSWORD, USER_ALREADY_EXISTS, INVALID_CREDENTIALS,
    INVALID_LIMIT_VALUE, INVALID_OFFSET_VALUE, INVALID_USER_ID
)
import json
from django.http import response
from friends.interactors.presenter_interface.user_presenter_interface import UserPresenterInterface


class UserSignUpPresenterImplementation(UserPresenterInterface):

    def created_user_id_response(self, user_id: int):
        response_dict = {
            "user_id": str(user_id)
        }
        data = json.dumps(response_dict)
        responses = response.HttpResponse(data, status=201)
        return responses

    def raise_invalid_password_exception(self):
        invalid_password_dict = {
            "response": INVALID_PASSWORD[0],
            "http_status_code": 400,
            "res_status": INVALID_PASSWORD[1]
        }
        data = json.dumps(invalid_password_dict)
        responses = response.HttpResponse(data, status=400)
        return responses

    def raise_invalid_email_id_exception(self):
        invalid_email_id_dict = {
            "response": INVALID_EMAIL_ID[0],
            "http_status_code": 400,
            "res_status": INVALID_EMAIL_ID[1]
        }
        data = json.dumps(invalid_email_id_dict)
        responses = response.HttpResponse(data, status=400)
        return responses

    def raise_user_already_exists_exception(self):
        user_already_exists_dict = {
            "response": USER_ALREADY_EXISTS[0],
            "http_status_code": 400,
            "res_status": USER_ALREADY_EXISTS[1]
        }
        data = json.dumps(user_already_exists_dict)
        responses = response.HttpResponse(data, status=400)
        return responses

    def get_access_token_response(self, access_token_dto):
        access_token_response = {
            "user_id": str(access_token_dto.user_id),
            "access_token": access_token_dto.access_token,
            "refresh_token": access_token_dto.refresh_token,
            "expires_in": str(access_token_dto.expires_in)
        }
        data = json.dumps(access_token_response)
        responses = response.HttpResponse(data, status=200)
        return responses

    def raise_invalid_credentials(self):
        invalid_credential_dict = {
            "response": INVALID_CREDENTIALS[0],
            "http_status_code": 400,
            "res_status": INVALID_CREDENTIALS[1]
        }
        data = json.dumps(invalid_credential_dict)
        responses = response.HttpResponse(data, status=400)
        return responses

    def raise_invalid_offset_error(self):
        user_not_authorised_dict = {
            "response": INVALID_OFFSET_VALUE[0],
            "http_status_code": 404,
            "res_status": INVALID_OFFSET_VALUE[1]
        }
        data = json.dumps(user_not_authorised_dict)
        responses = response.HttpResponse(data, status=404)
        return responses

    def raise_invalid_limit_error(self):
        user_not_authorised_dict = {
            "response": INVALID_LIMIT_VALUE[0],
            "http_status_code": 404,
            "res_status": INVALID_LIMIT_VALUE[1]
        }
        data = json.dumps(user_not_authorised_dict)
        responses = response.HttpResponse(data, status=404)
        return responses

    def get_all_users_response(self, search_users_result_dtp):
        total_count = search_users_result_dtp.total_count
        user_dtos = search_users_result_dtp.user_dtos

        search_user_result_list = self._get_user_response_list(user_dtos=user_dtos)
        response_dict = dict()
        response_dict["total_count"] = total_count
        response_dict["users"] = search_user_result_list
        data = json.dumps(response_dict)
        responses = response.HttpResponse(data, status=200)
        return responses

    @staticmethod
    def _get_user_response_list(user_dtos):
        response_user_list = []
        for user_dto in user_dtos:
            user_dict = dict()
            user_dict['user_id'] = str(user_dto.user_id)
            user_dict['email_id'] = user_dto.email_id
            user_dict['name'] = user_dto.name
            user_dict['is_admin'] = user_dto.is_admin
            response_user_list.append(user_dict)
        return response_user_list

    def raise_invalid_user_id_exception(self):
        invalid_user_id_dict = {
            "response": INVALID_USER_ID[0],
            "http_status_code": 404,
            "res_status": INVALID_USER_ID[1]
        }
        data = json.dumps(invalid_user_id_dict)
        responses = response.HttpResponse(data, status=404)
        return responses

    def get_pending_friends_requests(self, pending_request_result_dto):
        total_count = pending_request_result_dto.total_count
        user_dtos = pending_request_result_dto.user_dtos

        search_user_result_list = self._get_user_response_list(user_dtos=user_dtos)
        response_dict = dict()
        response_dict["total_count"] = total_count
        response_dict["users"] = search_user_result_list
        data = json.dumps(response_dict)
        responses = response.HttpResponse(data, status=200)
        return responses
