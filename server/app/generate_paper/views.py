from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .utils import res_common
from .services import aisv
from .serializer import GenerateAbstractSerializer, RefactorAbstractSerializer




class GeneratePaperView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pass
        
class GenerateAbstractView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GenerateAbstractSerializer(data=request.data)
        if not serializer.is_valid():
            return res_common.get_response400(message=serializer.errors)

        return res_common.get_response200(
            data=aisv.generate_abstract(**serializer.validated_data)
        )

    def patch(self, request):
        serializer = RefactorAbstractSerializer(data=request.data)
        if not serializer.is_valid():
            return res_common.get_response400(message=serializer.errors)

        return res_common.get_response200(
            data=aisv.refactor_abstract(**serializer.validated_data)
        )


class GenerateSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pass

class GenerateBodyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pass


class GenerateAcknowledgementView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pass


class GenerateReferenceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pass
