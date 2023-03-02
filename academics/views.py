from django.shortcuts import render

# Create your views here.
from rest_framework import generics,status
from .models import Classroom
from .serializer import ClassroomSerializer
from account.permissions import IsAdmin
from account.models import Teacher
from rest_framework.response import Response


class ClassroomCreateView(generics.CreateAPIView):
    """
    This api creates a classroom 


Attribs:
    queryset                 : This attribute sets the queryset of Classroom
                               objects that will be used for this view. 
    serializer_class         : This attribute sets the serializer class
                               that will be used for this view. 
    permission_classes       : This attribute sets the permission 
                               classes that will be used for this view
    Classroom Object attrubtes : [teacher,standard,division]
    teacher                  : to store instance of Teacher
    classroom                : to store instance of Classroom
    serializer               : Instance of  ClassroomSerializer class


    """
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [IsAdmin,]

    def post(self, request, *args, **kwargs):
        teacher_id = request.data.get('teacher')
        standard = request.data.get('standard')
        division = request.data.get('division')
        try:
            teacher = Teacher.objects.get(user__id = teacher_id)    
            if Classroom.objects.filter(teacher=teacher).exists():
                return Response({'error':'This Teacher is already assigned to \
                                  another classs.'},
                                  status=status.HTTP_400_BAD_REQUEST)
            classroom = Classroom.objects.create(
                        teacher=teacher,
                        division=division,
                        standard=standard
            )
            serializer = ClassroomSerializer(classroom)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"dev_data":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



