import enum


class FriendRequestStatus(enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class FriendRequestAction(enum.Enum):
    SEND_REQUEST = "SEND_REQUEST"
    ACCEPT_REQUEST = "ACCEPT_REQUEST"
    REJECT_REQUEST = "REJECT_REQUEST"
