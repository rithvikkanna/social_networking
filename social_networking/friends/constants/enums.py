import enum


class FriendRequestStatus(enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class FriendRequestAction:
    SEND_REQUEST = "SEND_REQUEST"
    ACCEPT_REQUEST = "ACCEPT_REQUEST"
    REJECT_REQUEST = "REJECT_REQUEST"
