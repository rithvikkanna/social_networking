from abc import ABC, abstractmethod


class UserPresenterInterface(ABC):

    @abstractmethod
    def raise_invalid_password_exception(self):
        pass

    @abstractmethod
    def raise_invalid_email_id_exception(self):
        pass

    @abstractmethod
    def raise_user_already_exists_exception(self):
        pass

    @abstractmethod
    def created_user_id_response(self, user_id:str):
        pass

    @abstractmethod
    def raise_invalid_credentials(self):
        pass

    @abstractmethod
    def get_access_token_response(self, access_token_dto):
        pass

    @abstractmethod
    def get_all_users_response(self, search_users_result_dtp):
        pass

    @abstractmethod
    def raise_invalid_offset_error(self):
        pass

    @abstractmethod
    def raise_invalid_limit_error(self):
        pass

    @abstractmethod
    def raise_invalid_user_id_exception(self):
        pass

