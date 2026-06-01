from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .utils import res_common
from .services import aisv
from .serializer import (
    GeneratePaperSerializer,
    GenerateAbstractSerializer,
    GenerateBodySerializer,
    GenerateSummarySerializer,
    GenerateAcknowledgementSerializer,
    GenerateReferenceSerializer,
)
from ..tools.ai import AIServiceError


class GeneratePaperView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GeneratePaperSerializer(data=request.data)
        if not serializer.is_valid():
            return res_common.get_response400(message=serializer.errors)

        try:
            return res_common.get_response200(
                data=aisv.generate_paper(user=request.user, **serializer.validated_data)
            )
        except AIServiceError as exc:
            return res_common.get_response502(message=str(exc))


class GenerateAbstractView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GenerateAbstractSerializer(data=request.data)
        if not serializer.is_valid():
            return res_common.get_response400(message=serializer.errors)

        try:
            return res_common.get_response200(
                data=aisv.generate_abstract(user=request.user, **serializer.validated_data)
            )
        except AIServiceError as exc:
            return res_common.get_response502(message=str(exc))


class GenerateSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GenerateSummarySerializer(data=request.data)
        if not serializer.is_valid():
            return res_common.get_response400(message=serializer.errors)

        try:
            return res_common.get_response200(
                data=aisv.generate_summary(user=request.user, **serializer.validated_data)
            )
        except AIServiceError as exc:
            return res_common.get_response502(message=str(exc))


class GenerateBodyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GenerateBodySerializer(data=request.data)
        if not serializer.is_valid():
            return res_common.get_response400(message=serializer.errors)

        try:
            return res_common.get_response200(
                data=aisv.generate_body(user=request.user, **serializer.validated_data)
            )
        except AIServiceError as exc:
            return res_common.get_response502(message=str(exc))


class GenerateAcknowledgementView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GenerateAcknowledgementSerializer(data=request.data)
        if not serializer.is_valid():
            return res_common.get_response400(message=serializer.errors)

        try:
            return res_common.get_response200(
                data=aisv.generate_acknowledgement(user=request.user, **serializer.validated_data)
            )
        except AIServiceError as exc:
            return res_common.get_response502(message=str(exc))


class GenerateReferenceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GenerateReferenceSerializer(data=request.data)
        if not serializer.is_valid():
            return res_common.get_response400(message=serializer.errors)

        try:
            return res_common.get_response200(
                data=aisv.generate_reference(user=request.user, **serializer.validated_data)
            )
        except AIServiceError as exc:
            return res_common.get_response502(message=str(exc))
