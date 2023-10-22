from dataclasses import dataclass
import datetime
from typing import List


@dataclass
class UserDto:
    user_id: str
    email_id: str
    name: str



@dataclass
class UserAuthDTO:
    user_id: int
    access_token: str
    refresh_token: str
    expires_in: datetime.datetime


@dataclass
class SearchUserResultDTO:
    user_dtos: List[UserDto]
    total_count: int
