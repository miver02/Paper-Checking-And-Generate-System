from django.urls import path
from .views import (
    GeneratePaperView, GenerateAbstractView, GenerateSummaryView,
    GenerateBodyView, GenerateAcknowledgementView, GenerateReferenceView
)

urlpatterns = [
    path('all/', GeneratePaperView.as_view(), name='generate_paper'),
    path('abstract/', GenerateAbstractView.as_view(), name='generate_abstract'),
    path('body/', GenerateBodyView.as_view(), name='generate_body'),
    path('summary/', GenerateSummaryView.as_view(), name='generate_summary'),
    path('acknowledgement/', GenerateAcknowledgementView.as_view(), name='generate_acknowledgement'),
    path('reference/', GenerateReferenceView.as_view(), name='generate_reference'),
]