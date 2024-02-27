from enum import Enum

LOBBY_WS_GROUP_NAME = 'lobby'
ROOMS_WS_GROUP_NAME = 'room_'


class EventType:
    room_created = 'room_created'


class ErrorType(Enum):
    ROOM_EXISTS = 'Room Name'


class ErrorMsg(Enum):
    ROOM_EXISTS = 'Room already exists'


class FormError:

    @staticmethod
    def get_error(error_type: ErrorType):
        error_type = error_type
        error_msg = ErrorMsg[error_type.name]
        return (
            {
                'error_type': error_type.value,
                'error_msg': error_msg.value
            }
        )
