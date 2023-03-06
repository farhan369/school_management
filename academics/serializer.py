from rest_framework import serializers
from account.models import Teacher, Account
from django.contrib.auth.models import User
from .models import Classroom, Exam, Question, Option, Response as Responsee
from rest_framework.response import Response
from rest_framework import status


class ClassroomSerializer(serializers.ModelSerializer):
    # this serilizer is for Classroom model
    teacher_id = serializers.IntegerField()

    class Meta:
        model = Classroom
        fields = ["id", "standard", "division", "teacher_id"]


class ExamSerilalizer(serializers.ModelSerializer):
    # this serializer is for Exam model
    classroom_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Exam
        fields = ["id", "name", "start_time", "end_time", "classroom_id"]

    def create(self, validated_data):
        try:
            request = self.context.get("request")
            classroom_id = request.parser_context["kwargs"].get("id")
            classroom = Classroom.objects.get(id=classroom_id)
            exam = Exam.objects.create(classroom=classroom, **validated_data)
            return exam
        except Exception as e:
            return Response(
                {"error": "something went wrong", "dev_deta": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


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
        fields = ('id', 'text', 'options')

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