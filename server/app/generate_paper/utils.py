from rest_framework.response import Response
from rest_framework import status

class ResponseCommon:
    """
    响应数据结构
    """
    def __init__(self):
        pass

    def get_response200(self, message: str = '请求成功', data: any = None):
        return Response({
            "code": status.HTTP_200_OK,
            "message": message,
            "data": data
        })

    def get_response400(self, message: str):
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': message,
            'data': {}
        })
    
    def get_response401(self):
        return Response({
            'code': status.HTTP_401_UNAUTHORIZED,
            'message': 'Unauthorized',
            'data': {}
        })

    def get_response403(self, message: str):
        return Response({
            'code': status.HTTP_403_FORBIDDEN,
            'message': message,
            'data': {}
        }, status=status.HTTP_403_FORBIDDEN)

    def get_response404(self, message: str):
        return Response({
            'code': status.HTTP_404_NOT_FOUND,
            'message': message,
            'data': {}
        }, status=status.HTTP_404_NOT_FOUND)

    def get_response502(self, message: str):
        return Response({
            'code': status.HTTP_502_BAD_GATEWAY,
            'message': message,
            'data': {}
        }, status=status.HTTP_502_BAD_GATEWAY)


res_common = ResponseCommon()
