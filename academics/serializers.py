from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from account import models as account_models
from . import models as academics_models


class ClassTeacherSerializer(serializers.ModelSerializer):
    """
    this serializer is used as nested in classroom
    serializer to print teachers data 
    """
    username = serializers.CharField(source="user.user.username") 
    class Meta:
        model = account_models.Teacher
        fields = '__all__'


class ClassroomSerializer(serializers.ModelSerializer):
    """
    this serializer is for classroom model
    """
    teacher_username = serializers.CharField(write_only=True)
    teacher = ClassTeacherSerializer(read_only = True)
    class Meta:
        model = academics_models.Classroom
        fields = ["id", "standard", "division", "teacher_username","teacher"]
    
    def create(self, validated_data):
        """
        modifying to identify teacher object by username
        """
        teacher_username = validated_data.pop('teacher_username')
        teacher = account_models.Teacher.objects.get(user__user__username = teacher_username)
        classroom = academics_models.Classroom.objects.create(teacher=teacher,**validated_data)
        return classroom



class ExamSerilalizer(serializers.ModelSerializer):
    """
    serializer for Exam model
    """
    classroom_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = academics_models.Exam
        fields = ["id", "name", "start_time", "end_time", "classroom_id"]

    def create(self, validated_data):
        """
        overriden to take classroom_id from url
        """
        request = self.context.get("request")
        classroom_id = request.parser_context["kwargs"].get("id")
        classroom = academics_models.Classroom.objects.get(id=classroom_id)
        exam = academics_models.Exam.objects.create(classroom=classroom, **validated_data)
        return exam


class OptionSerializer(serializers.ModelSerializer):
    """
    This serializer is for options model
    """
    class Meta:
        model = academics_models.Option
        fields = ('id', 'text', 'is_correct')


class QuestionSerializer(serializers.ModelSerializer):
    """
    This serializer is used to create question and options
    of a exam in the database
    Attributes:
        exam_id = used to store the exam_id taken from url
        options = serializer instance for options Model
    """
    options = OptionSerializer(many=True)

    class Meta:
        model = academics_models.Question
        fields = ('id', 'text', 'options','mark')

    def create(self, validated_data):
        """
        overriden to create options along with creating questions
        """
        options_data = validated_data.pop('options')
        exam_id = self.context['view'].kwargs.get('exam_id')
        exam = academics_models.Exam.objects.get(id=exam_id)
        question = academics_models.Question.objects.create(exam = exam,**validated_data)
        for option_data in options_data:
            academics_models.Option.objects.create(question=question, **option_data)
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
        model = academics_models.Response
        fields = ['option','student_id','options']

    def create(self, validated_data):
        """
        overriden to get  student object from token and to 
        add multiple option selected by user in options field in Response
        """
        student = self.context['request'].user.account.student 
        question_id = self.context['view'].kwargs.get('question_id')
        question = academics_models.Question.objects.get(id=question_id)
        responses = academics_models.Response.objects.filter(
            student=student,option__question = question).all()
        # Checks if the student already answered this question
        if responses:
            return Response({"message":'already answered this question'})

        options_data = validated_data.pop('options')
        print(options_data)
        response =  academics_models.Response.objects.create(student=student,**validated_data)
        for option_data in options_data:
            option = academics_models.Option.objects.get(id=option_data)
            response.option.add(option)
        return response
    

class ExamResultSerializer(serializers.Serializer):
        """
        Serializer to show the result of a student 
        with student_username,exam_name,standard,division,
        total mark,score.
        Attributes:
            exam = name of exam
            standard = standard of the student
            division = division of the student
            username = username of the student
            total_mark = max mark that can be obtained in that exam
            score = mark obtained by that student
        """
        def to_representation(self, instance):
            ret = dict()
            exam_id = instance.id
            student_id = self.context['view'].kwargs.get('student_id')
            exam = academics_models.Exam.objects.get(id=exam_id)
            student = account_models.Student.objects.get(
                user__user__id=student_id)
            ret['exam'] = exam.name
            ret['standard'] = exam.classroom.standard
            ret['division'] = exam.classroom.division
            ret['username'] = student.user.user.username
            questions = academics_models.Question.objects.filter(exam=exam)
            mark = 0
            for question in questions:
                mark = mark + question.mark
            ret['total_mark'] = mark # max mark that can be scored
            responses = academics_models.Response.objects.filter(
                student=student,option__question__exam =exam)
            score =0
            for response in responses:
                score = score + response.option.filter(is_correct=True).count()
            ret['score'] = score #mark of the student
            return ret
            

