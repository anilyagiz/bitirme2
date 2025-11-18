"""Custom exceptions for the application"""

from typing import Any, Dict, Optional


class AppException(Exception):
    """Base exception for application-specific errors"""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


# Authentication & Authorization Exceptions
class AuthenticationError(AppException):
    """Authentication failed"""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


class InvalidCredentialsError(AuthenticationError):
    """Invalid email or password"""

    def __init__(self):
        super().__init__("Incorrect email or password")


class InactiveUserError(AuthenticationError):
    """User account is inactive"""

    def __init__(self):
        super().__init__("User account is inactive")


class AuthorizationError(AppException):
    """Not enough permissions"""

    def __init__(self, message: str = "Not enough permissions"):
        super().__init__(message, status_code=403)


# Resource Exceptions
class ResourceNotFoundError(AppException):
    """Resource not found"""

    def __init__(self, resource_name: str, resource_id: Optional[str] = None):
        message = f"{resource_name} not found"
        if resource_id:
            message += f" (ID: {resource_id})"
        super().__init__(message, status_code=404)


class ResourceAlreadyExistsError(AppException):
    """Resource already exists"""

    def __init__(self, resource_name: str, field: str, value: str):
        super().__init__(
            f"{resource_name} with {field} '{value}' already exists",
            status_code=409
        )


# Business Logic Exceptions
class InvalidOperationError(AppException):
    """Invalid operation for current state"""

    def __init__(self, message: str):
        super().__init__(message, status_code=409)


class ValidationError(AppException):
    """Validation failed"""

    def __init__(self, message: str, field: Optional[str] = None):
        details = {"field": field} if field else {}
        super().__init__(message, status_code=422, details=details)


# User-specific Exceptions
class UserNotFoundError(ResourceNotFoundError):
    """User not found"""

    def __init__(self, user_id: Optional[str] = None):
        super().__init__("User", user_id)


class UserAlreadyExistsError(ResourceAlreadyExistsError):
    """User with email already exists"""

    def __init__(self, email: str):
        super().__init__("User", "email", email)


class WeakPasswordError(ValidationError):
    """Password does not meet security requirements"""

    def __init__(self, message: str = "Password does not meet security requirements"):
        super().__init__(message, field="password")


# Assignment-specific Exceptions
class AssignmentNotFoundError(ResourceNotFoundError):
    """Assignment not found"""

    def __init__(self, assignment_id: Optional[str] = None):
        super().__init__("Assignment", assignment_id)


class InvalidAssignmentStateError(InvalidOperationError):
    """Assignment is not in valid state for this operation"""

    def __init__(self, message: str):
        super().__init__(message)


# Building-specific Exceptions
class BuildingNotFoundError(ResourceNotFoundError):
    """Building not found"""

    def __init__(self, building_id: Optional[str] = None):
        super().__init__("Building", building_id)


class BuildingAlreadyExistsError(ResourceAlreadyExistsError):
    """Building with name already exists"""

    def __init__(self, name: str):
        super().__init__("Building", "name", name)


# Department-specific Exceptions
class DepartmentNotFoundError(ResourceNotFoundError):
    """Department not found"""

    def __init__(self, department_id: Optional[str] = None):
        super().__init__("Department", department_id)


class DepartmentAlreadyExistsError(ResourceAlreadyExistsError):
    """Department with name already exists"""

    def __init__(self, name: str):
        super().__init__("Department", "name", name)


# Location-specific Exceptions
class LocationNotFoundError(ResourceNotFoundError):
    """Location not found"""

    def __init__(self, location_id: Optional[str] = None):
        super().__init__("Location", location_id)


class InvalidLocationError(InvalidOperationError):
    """Invalid location for this operation"""

    def __init__(self, message: str):
        super().__init__(message)


# Period-specific Exceptions
class PeriodNotFoundError(ResourceNotFoundError):
    """Period not found"""

    def __init__(self, period_id: Optional[str] = None):
        super().__init__("Period", period_id)


class NoPeriodActiveError(AppException):
    """No active period found"""

    def __init__(self):
        super().__init__("No active period found", status_code=404)
