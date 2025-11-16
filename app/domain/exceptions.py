"""Domain exceptions for the application."""


class DomainException(Exception):
    """Base exception for domain errors."""

    def __init__(self, message: str, code: str | None = None):
        self.message = message
        self.code = code or self.__class__.__name__
        super().__init__(self.message)


class EntityNotFoundError(DomainException):
    """Raised when an entity is not found."""

    def __init__(self, entity_name: str, identifier: str | int):
        message = f"{entity_name} with id '{identifier}' not found"
        super().__init__(message, "ENTITY_NOT_FOUND")


class ValidationError(DomainException):
    """Raised when domain validation fails."""

    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR")


class BusinessRuleViolationError(DomainException):
    """Raised when a business rule is violated."""

    def __init__(self, message: str):
        super().__init__(message, "BUSINESS_RULE_VIOLATION")

