import datetime

from friends.interactors.storage_interface.friends_storage_interface import FriendStorageInterface
from friends.models import Friends
from django.db.models import Q
from friends.constants.enums import FriendRequestStatus
from friends.interactors.dtos.friends_dtos import FriendDTO, FriendRequestsResultDTO, PendingRequestsResultDTO, \
    FriendRequestDTO


class FriendsStorage(FriendStorageInterface):

    def get_user_friends(self, user_id: str, limit: int, offset: int):
        accepted_requests = Friends.objects.filter(
            (Q(sender_id=user_id) | Q(recipient_id=user_id)) & Q(status=FriendRequestStatus.ACCEPTED.value)
        ).select_related('sender', 'recipient')

        friends_list = self._get_friends_list(friends=accepted_requests, user_id=user_id)
        total_count = len(friends_list)
        friend_dtos = self._convert_friend_request_obj_to_friend_dtos(
            friend_requests=friends_list[offset: offset + limit])
        friend_request_result_dto = FriendRequestsResultDTO(
            total_count=total_count,
            friend_requests=friend_dtos
        )
        return friend_request_result_dto

    def get_user_pending_friend_requests(self, user_id, limit: int, offset: int):

        pending_requests = Friends.objects.filter(
            recipient=user_id, status=FriendRequestStatus.PENDING.value
        ).select_related('sender', 'recipient')

        request_friend_objs = self._get_requested_friends(pending_requests=pending_requests)
        total_count = pending_requests.count()
        friend_dtos = self._convert_friend_request_obj_to_friend_dtos(
            friend_requests=request_friend_objs[offset: offset + limit])
        pending_request_result_dto = PendingRequestsResultDTO(
            total_count=total_count,
            pending_requests=friend_dtos
        )
        return pending_request_result_dto

    def accept_friend_request(self, friend_request_accepted_user_id: str, friend_request_sent_user_id: str):
        friend_request_obj = Friends.objects.filter(sender_id=friend_request_sent_user_id,
                                                    recipient_id=friend_request_accepted_user_id).update(
            status=FriendRequestStatus.ACCEPTED.value)

    def send_friend_request(self, friend_request_received_user_id: str, friend_request_sent_user_id: str):
        friend_request_obj = Friends.objects.filter(sender_id=friend_request_sent_user_id,
                                                    recipient_id=friend_request_received_user_id).update(
            status=FriendRequestStatus.PENDING.value)

    def reject_friend_request(self, friend_request_rejected_user_id: str, friend_request_sent_user_id: str):
        friend_request_obj = Friends.objects.filter(sender_id=friend_request_sent_user_id,
                                                    recipient_id=friend_request_rejected_user_id).update(
            status=FriendRequestStatus.REJECTED.value)

    def get_user_requests_by_status(self, friend_request_sent_user_id: str, friend_request_received_user_id: str,
                                    status: FriendRequestStatus):
        friend_request_obj = Friends.objects.filter(sender_id=friend_request_sent_user_id,
                                                    recipient_id=friend_request_received_user_id, status=status)

        friend_request_dtos = self._convert_friend_request_objs_to_dtos(friend_request_obj)

        return friend_request_dtos

    def get_user_send_friend_request(self, user_id: str, requested_at: datetime.datetime):

        user_requested_friends_requests = Friends.objects.filter(sender_id=user_id,

                                                                 requested_at__gte=requested_at
                                                                 )

        friend_request_dto = self._convert_friend_request_objs_to_dtos(user_requested_friends_requests)
        return friend_request_dto

    def _get_friends_list(self, friends, user_id: str):
        friends_list = []

        for friend in friends:
            if friend.sender_id == user_id:

                friends_list.append(friend.recipient)
            else:

                friends_list.append(friend.sender)
        return friends_list

    def _convert_friend_request_obj_to_friend_dtos(self, friend_requests):
        friend_dtos = []

        for friend_request in friend_requests:
            friend_dto = FriendDTO(
                user_id=friend_request.user_id,
                email_id=friend_request.email_id,
                name=friend_request.name,
                is_admin=friend_request.is_admin
            )
            friend_dtos.append(friend_dto)
        return friend_dtos

    def _get_requested_friends(self, pending_requests):
        request_user_objs = []
        for pending_request in pending_requests:
            request_user_objs.append(pending_request.sender)
        return request_user_objs

    def _convert_friend_request_objs_to_dtos(self, friend_request_objs):

        friend_request_dtos = []

        for friend_request in friend_request_objs:
            friend_request_dto = FriendRequestDTO(
                sender_user_id=friend_request.sender_id,
                receiver_user_id=friend_request.recipient_id,
                status=friend_request.status,
                requested_at=friend_request.requested_at
            )
            friend_request_dtos.append(friend_request_dto)
        return friend_request_dtos

    def check_existing_user_request(self, sender_user_id: str, receiver_user_id: str):
        fiends_objs = Friends.objects.filter((Q(sender_id=sender_user_id) | Q(recipient_id=sender_user_id)) & (
                Q(sender_id=receiver_user_id) | Q(recipient_id=receiver_user_id)))

        friend_request_dtos = self._convert_friend_request_objs_to_dtos(fiends_objs)

        return friend_request_dtos
