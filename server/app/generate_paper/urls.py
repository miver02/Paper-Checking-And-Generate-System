from django.urls import path
from .views import (
    GeneratePaperView,
    GeneratePaperStatusView,
    GenerateAbstractView,
    GenerateSummaryView,
    GenerateBodyView,
    GenerateAcknowledgementView,
    GenerateReferenceView,
)

urlpatterns = [
    path('all/', GeneratePaperView.as_view(), name='generate_paper'),
    path('<int:paper_id>/status/', GeneratePaperStatusView.as_view(), name='generate_paper_status'),
    path('abstract/', GenerateAbstractView.as_view(), name='generate_abstract'),
    path('body/', GenerateBodyView.as_view(), name='generate_body'),
    path('summary/', GenerateSummaryView.as_view(), name='generate_summary'),
    path('acknowledgement/', GenerateAcknowledgementView.as_view(), name='generate_acknowledgement'),
    path('reference/', GenerateReferenceView.as_view(), name='generate_reference'),
]
