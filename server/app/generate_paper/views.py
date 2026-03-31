from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .utils import res_common
from ..tools import AIToolClass
from .services import aisv


aitc = AIToolClass()

class GeneratePaperView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pass
        
class GenerateAbstractView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        abstract_text = request.data.get('abstract', None)  # 默认值为None

        if abstract_text is not None and not isinstance(abstract_text, str):
            return res_common.get_response400(message="Abstract must be a string or None.")

        if abstract_text is None:
            return res_common.get_response200(message="Abstract is None.")
        

        return res_common.get_response200(data=aitc.get_ai_response(aisv.generate_abstract(abstract_text)))


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
