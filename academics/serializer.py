from rest_framework import serializers
from account.models import Teacher, Account, Student
from django.contrib.auth.models import User
from .models import Classroom, Exam, Question, Option, Response as Responsee
from rest_framework.response import Response
from rest_framework import status


class ClassTeacherSerializer(serializers.ModelSerializer):
    """this serializer is used as nested in classroom
        serializer to print teachers data 
    """
    username = serializers.CharField(source="user.user.username") 
    class Meta:
        model = Teacher
        fields = '__all__'


class ClassroomSerializer(serializers.ModelSerializer):
    # this serilizer is for Classroom model
    teacher_username = serializers.CharField(write_only=True)
    teacher = ClassTeacherSerializer(read_only = True)
    class Meta:
        model = Classroom
        fields = ["id", "standard", "division", "teacher_username","teacher"]
    
    def create(self, validated_data):
        """
        modifying to identify teacher object by username
        """
        print(validated_data)
        teacher_username = validated_data.pop('teacher_username')
        teacher = Teacher.objects.get(user__user__username = teacher_username)
        classroom = Classroom.objects.create(teacher=teacher,**validated_data)
        return classroom



class ExamSerilalizer(serializers.ModelSerializer):
    # this serializer is for Exam model
    classroom_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Exam
        fields = ["id", "name", "start_time", "end_time", "classroom_id"]

    def create(self, validated_data):
        
            request = self.context.get("request")
            classroom_id = request.parser_context["kwargs"].get("id")
            classroom = Classroom.objects.get(id=classroom_id)
            exam = Exam.objects.create(classroom=classroom, **validated_data)
            return exam


class OptionSerializer(serializers.ModelSerializer):
    """
    This serializer is for options model
    """
    class Meta:
        model = Option
        fields = ('id', 'text', 'is_correct')


class QuestionSerializer(serializers.ModelSerializer):
    """
    This serializer is used to create question and options
    of a exam in the database
    Attributes:
        exam_id = used to store the exam_id taken from url
    """
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'options','mark')

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        exam_id = self.context['view'].kwargs.get('exam_id')
        exam = Exam.objects.get(id=exam_id)
        question = Question.objects.create(exam = exam,**validated_data)
        for option_data in options_data:
            Option.objects.create(question=question, **option_data)
        return question


class ResponseSerializer(serializers.ModelSerializer):
    """
    This serializer is used for saving responses
    Attributes:
        options = to store id of all options
        responses = store respones of the question student is trying to answer
        options_data = store which all option ids the student marked
    """
    options = serializers.ListField(write_only=True)
    student_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Responsee
        fields = ['option','student_id','options']

    def create(self, validated_data):
        student = self.context['request'].user.account.student 
        question_id = self.context['view'].kwargs.get('question_id')
        question = Question.objects.get(id=question_id)
        responses = Responsee.objects.filter(
            student=student,option__question = question).all()
        # Checks if the student already answered this question
        if responses:
            return Response({"message":'already answered this question'})

        options_data = validated_data.pop('options')
        print(options_data)
        response = Responsee.objects.create(student=student,**validated_data)
        for option_data in options_data:
            option = Option.objects.get(id=option_data)
            response.option.add(option)
            print("hello")

        return response
    

class ExamResultSerializer(serializers.Serializer):
        exam_id  = serializers.IntegerField(read_only = True)
        student_id = serializers.IntegerField(read_only=True)
        total_questions = serializers.IntegerField(read_only=True)
        score = serializers.IntegerField(read_only=True)

        class Meta:
            fields = ('exam_id','student_id','total_mark','score')

        def to_representation(self, instance):
            ret = super().to_representation(instance)
            exam_id = self.context['view'].kwargs.get('exam_id')
            student_id = self.context['view'].kwargs.get('student_id')
            exam = Exam.objects.get(id=exam_id)
            print(exam)
            student = Student.objects.get(user__user__id=student_id)
            print(student)
            questions = Question.objects.filter(exam=exam)
            mark = 0
            for question in questions:
                mark = mark + question.mark
            ret['total_mark'] = mark
            responses = Responsee.objects.filter(student=student,option__question__exam =exam)
            print(responses)
            score =0
            for response in responses:
                score = score + response.option.filter(is_correct=True).count()
            ret['score'] = score
            return ret
            

