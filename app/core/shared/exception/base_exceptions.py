class CoreException(Exception):
    message: str

    def __init__(self, message: str):
        super().__init__(message)


class EntityNotFoundException(CoreException):
    """Raised when Entity is not found in DB"""


class InvalidStatusException(CoreException):
    """Raised when the entity is an unexpected status"""
