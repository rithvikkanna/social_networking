from dataclasses import dataclass
import datetime
from friends.constants.enums import FriendRequestStatus, FriendRequestAction


@dataclass
class FriendDTO:
    user_id: str
    email_id: str
    name: str
    is_admin: bool


@dataclass
class FriendRequestDTO:
    sender_user_id: str
    receiver_user_id: str
    status: FriendRequestStatus
    requested_at: datetime.datetime


@dataclass
class FriendRequestsResultDTO:
    friend_requests: [FriendDTO]
    total_count: int


@dataclass
class PendingRequestsResultDTO:
    pending_requests: [FriendDTO]
    total_count: int


@dataclass
class FriendRequestParamsDTO:
    action: FriendRequestAction
    sender_user_id: str
    receiver_user_id: str

