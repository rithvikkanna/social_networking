from friends.interactors.storage_interface.user_storage_interface import UserStorageInterface
from friends.models import User
from friends.interactors.dtos.user_dtos import UserDto, SearchUserResultDTO
from django.contrib.auth.hashers import check_password


class UserStorageImplementation(UserStorageInterface):
    def validate_email_id(self, email_id: str):
        try:
            user_objs = User.objects.filter(email=email_id)
        except User.DoesNotExist:
            return False
        user_dtos = self._convert_user_objects_into_user_dtos(user_objs=user_objs)
        return user_dtos

    def validate_user_password(self, email_id: str, password: str):
        user_obj = User.objects.get(email=email_id)
        is_valid_password = not check_password(password, user_obj.password)
        print(is_valid_password)
        return is_valid_password

    def create_user(self, email_id: str, password: str, name: str):

        user_obj = User.objects.create(email=email_id, password=password, name=name)

        user_dto = self._convert_user_object_into_dto(user_obj=user_obj)
        return user_dto

    @staticmethod
    def _convert_user_object_into_dto(user_obj):

        user_dto = UserDto(user_id=user_obj.user_id, name=user_obj.name, email_id=user_obj.email
                           )
        return user_dto

    def get_users_by_name(self, search_query: str, limit: int, offset: int):
        user_obj = User.objects.filter(name__icontains=search_query)

        total_count = user_obj.count()
        paginated_user_dtos = self._convert_user_objects_into_user_dtos(user_obj[offset: offset + limit])
        search_users_result_dto = SearchUserResultDTO(
            user_dtos=paginated_user_dtos,
            total_count=total_count
        )
        return search_users_result_dto

    @staticmethod
    def _convert_user_objects_into_user_dtos(user_objs):


        user_dtos = [
            UserDto(user_id=user_obj.user_id, name=user_obj.name, email_id=user_obj.email)
            for user_obj in user_objs]
        return user_dtos
