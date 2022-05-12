class CoreException(Exception):
    message: str

    def __init__(self, message: str):
        super().__init__(message)


class EntityNotFoundException(CoreException):
    """Raised when Entity is not found in DB"""


class EntityAlreadyExistsException(CoreException):
    """Raised when Entity already exists in DB"""


class EntityPersistException(CoreException):
    """Raised when persisting the Entity in DB fails"""


class InvalidStatusException(CoreException):
    """Raised when the entity is an unexpected status"""


class AuthException(CoreException):
    """Raised when user authentication fails"""
