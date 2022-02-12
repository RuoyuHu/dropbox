from enum import Enum


"""
    Enum of accepted request types, constant across system
"""
class RequestType(Enum):
    CREATE = 0
    UPDATE = 1
    DELETE = 2

    def send_data(self):
        return self in [
            RequestType.CREATE,
            RequestType.UPDATE,
        ]

