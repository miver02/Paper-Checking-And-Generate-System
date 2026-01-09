from rest_framework.response import Response
from rest_framework import status


class ResponseCommon:
    """
    响应数据结构
    """

    def __init__(self):
        pass

    def get_response200(self, message: str, data: dict = None):
        return Response({
            "code": status.HTTP_200_OK,
            "message": message,
            "data": data
        })

    def get_response400(self, err: str):
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': err,
            'data': {}
        })
    
    def get_response401(self):
        return Response({
            'code': status.HTTP_401_UNAUTHORIZED,
            'message': 'Unauthorized',
            'data': {}
        })


res_common = ResponseCommon()
