from rest_framework import generics
from django_filters import rest_framework as filters
from . import models as academics_models

class ExamStandardFilter(filters.FilterSet):
    exam_name = filters.CharFilter(field_name='exam__name')
    academic_year = filters.CharFilter(
        field_name='exam__academics_year__start_year')
    standard = filters.CharFilter(field_name='standard__name')

    class Meta:
        model = academics_models.ExamStandard
        fields = ['exam_name', 'academic_year', 'standard']


class ExamStandardSubjectFilter(filters.FilterSet):
    exam_standard = filters.NumberFilter(field_name='exam_standard')
    subject = filters.CharFilter(field_name='subject__name')

    class Meta:
        model = academics_models.ExamStandardSubject
        fields = ['exam_standard', 'subject']