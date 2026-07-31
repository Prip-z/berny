class DomainError(Exception):
    pass


class UserAlreadyExistsError(DomainError):
    pass


class UserNotFoundError(DomainError):
    pass


class TokenExpired(DomainError):
    pass

class InvalidToken(DomainError):
    pass

class InvalidPassword(DomainError):
    pass