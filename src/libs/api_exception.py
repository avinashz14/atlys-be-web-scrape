from rest_framework import exceptions, status

# from libs.app_logger import AppLogger
#
# logger = AppLogger(tag="API Exception")


class Unauthorized(exceptions.APIException):
    status_code = 401
    default_code = "unauthorized"
    default_detail = "Unauthorized"


class PermissionDenied(exceptions.APIException):
    status_code = 401
    default_code = "Permission Denied"
    default_detail = "Permission Denied"


class NotFound(exceptions.APIException):
    status_code = 404
    default_code = "Not Found"
    default_detail = "Not Found"


class BadRequest(exceptions.APIException):
    status_code = 400
    default_code = "Bad Request"
    default_detail = "Bad Request"


class CustomError(exceptions.APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "A server error occurred."

    def __init__(self, data, status_code):
        if status_code is not None:
            self.status_code = status_code

        if data is not None:
            self.detail = data
        else:
            self.detail = {
                "status": 0,
                "message": self.default_detail,
            }
