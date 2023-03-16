import django_filters

from . import models as account_models


class StudentFilterSet(django_filters.FilterSet):
    """
    filter used to get student of a specific standard or specific class
    """
    standard = django_filters.CharFilter(
        field_name='classroom__standard')
    division = django_filters.CharFilter(
        field_name='classroom__division')

    class Meta:
        model = account_models.Student
        fields = ('classroom',)


class TeacherFilter(django_filters.FilterSet):
    """
    filter used to get teacher of a specific standard or specific class
    """
    standard = django_filters.NumberFilter(field_name='classroom__standard')
    division = django_filters.CharFilter(field_name='classroom__division')

    class Meta:
        model = account_models.Teacher
        fields = ['standard', 'division']