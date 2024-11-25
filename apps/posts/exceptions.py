from rest_framework.exceptions import APIException


class PostNotFound(APIException):
    status_code = 404
    deafult_detail = "The requested post does not exist"
