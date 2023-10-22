from typing import List
from friends.exceptions.exceptions import InvalidLimitValue, InvalidOffsetValue, InvalidUserID


class ValidationMixin:

    @staticmethod
    def validate_limit_value(limit: int):
        if limit < 1:
            raise InvalidLimitValue

    @staticmethod
    def validate_offset_value(offset: int):
        if offset < 0:
            raise InvalidOffsetValue

    @staticmethod
    def validate_user_ids(user_ids: List[str], user_storage):
        user_dtos = user_storage.validate_user_ids(user_ids=user_ids)
        if len(user_ids != user_dtos):
            raise InvalidUserID

