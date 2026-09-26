class AppException(Exception):

    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code


class NotFoundException(AppException):

    def __init__(
        self,
        message: str,
        error_code: str
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=404
        )


class BadRequestException(AppException):

    def __init__(
        self,
        message: str,
        error_code: str
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=400
        )


class UnauthorizedException(AppException):

    def __init__(
        self,
        message: str,
        error_code: str
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=401
        )


class ForbiddenException(AppException):

    def __init__(
        self,
        message: str,
        error_code: str
    ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=403
        )