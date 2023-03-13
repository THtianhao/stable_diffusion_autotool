from dataclasses import dataclass

@dataclass
class UserResponseData:
    access_token: str

@dataclass
class UserResponse:
    code: int
    msg: str
    data: UserResponseData
