from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from account import models as account_models

from . import models as academics_models

import datetime 

from rest_framework.exceptions import ValidationError


class AcademicYearSerilizer(serializers.ModelSerializer):
    """
    this serializer is used for creating an academics year
    """

    class Meta:
        """A class that defines metadata for a Django ModelForm"""
        
        model = academics_models.AcademicYear
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    """
    this serializer is used for creating a subject
    """

    class Meta:
        """A class that defines metadata for a Django ModelForm"""
        
        model = academics_models.Subject
        fields = '__all__'


class StandardSerializer(serializers.ModelSerializer):
    """
    this serializer is used for creating a standard
    """

    class Meta:
        """A class that defines metadata for a Django ModelForm"""
        
        model = academics_models.Standard
        fields = '__all__'


class ClassTeacherSerializer(serializers.ModelSerializer):
    """
    this serializer is used as nested in classroom
    serializer to print teachers data 
    """
    
    password = serializers.CharField(write_only=True)
    
    class Meta:
        """A class that defines metadata for a Django ModelForm"""
        
        model = account_models.Teacher
        fields = '__all__'


class ClassroomSerializer(serializers.ModelSerializer):
    """
    this serializer is for classroom model
    """
    
    teacher_username = serializers.CharField(write_only=True)
    teacher = ClassTeacherSerializer(read_only=True)
    academic_year_name = serializers.IntegerField(write_only=True)
    subjects_name = serializers.ListField(write_only=True)
    standard_name = serializers.IntegerField(write_only=True)
    
    class Meta:
        """A class that defines metadata for a Django ModelForm"""
        
        model = academics_models.Classroom
        fields = [
            "id", "standard", "division", "teacher_username","teacher",
            "academic_year","subjects","academic_year_name","subjects_name",
            "standard_name"]
        read_only_fields = ["id","standard", "academic_year","subjects",]
    
    def create(self, validated_data):
        """
        modifying to identify teacher object by username
        """
        
        teacher_username = validated_data.pop('teacher_username')
        academic_year = validated_data.pop('academic_year_name')
        standard = validated_data.pop('standard_name')
        subjects = validated_data.pop('subjects_name')
        try:
            validated_data['teacher'] = \
                account_models.Teacher.objects.get(username = teacher_username)
        except account_models.Teacher.DoesNotExist:
            raise ValidationError(
                {'message': 'Teacher with this username does not exist.'})
        try:
            validated_data['standard'] = \
                academics_models.Standard.objects.get(name=standard)
        except:
            raise ValidationError({"message":"standard doesn't exist"})    
        try:
            validated_data['academic_year'] = \
                academics_models.AcademicYear.objects.get(
                start_year=academic_year)
        except:
            raise ValidationError({"message":"academic year doesn't exist"})
        classroom = super().create(validated_data)
        for subject in subjects:
            try:
                subject = \
                    academics_models.Subject.objects.get(name=subject)
            except:
                raise ValidationError({"message":"standard doesn't exist"})
            classroom.subjects.add(subject)
        return classroom



class ExamSerilalizer(serializers.ModelSerializer):
    """
    serializer for Exam model
    """
    academic_year_name = serializers.IntegerField(write_only=True)
    standard_list = serializers.ListField(write_only=True)

    class Meta:
        """A class that defines metadata for a Django ModelForm"""
       
        model = academics_models.Exam
        fields = ["id", "name", "start_date", "end_date", "academics_year",
                  "standard", "academic_year_name", "standard_list"]
        read_only_fields = ["id","standard", "academic_year"]
    
    def create(self, validated_data):
        """
        to add standards who can take the exam
        """
        
        standards = validated_data.pop('standard_list')
        academic_year = validated_data.pop('academic_year_name')
        try:
            validated_data['academics_year'] = \
                academics_models.AcademicYear.objects.get(start_year=academic_year)
        except:
            raise ValidationError({"message":"enter a valid academic year"})
        exam = super().create(validated_data)
        for standard in standards:
            exam.standard.add(standard)
        return exam


class ExamStandardSerializer(serializers.ModelSerializer):
    """
    Serializer for Addmin Subject to ExamStandard Model
    """
    
    subjects_list = serializers.ListField(write_only=True)
    
    class Meta:
        """A class that defines metadata for a Django ModelForm"""
        
        model = academics_models.ExamStandard
        fields = ["id","exam","standard","subjects","subjects_list"]
        read_only_fields = ["id","standard", "exam","subjects"]

    def update(self, instance, validated_data):
        """to add subjects """

        subjects = validated_data.pop('subjects_list')
        for subject in subjects:
            try:
                subject = academics_models.Subject.objects.get(name=subject)
            except:
                raise ValidationError({"message":"subject not found"})
            instance.subjects.add(subject)
        return instance


class ExamStandardSubjectSerializer(serializers.ModelSerializer):
    """
    Serializer for ExamStandardSubject model
    """

    class Meta:
        """A class that defines metadata for a Django ModelForm"""
        
        model = academics_models.ExamStandardSubject
        fields = '__all__'


class OptionSerializer(serializers.ModelSerializer):
    """
    This serializer is for options model
    """
    
    class Meta:
        """A class that defines metadata for a Django ModelForm"""
        
        model = academics_models.Option
        fields = ('id', 'text', 'is_correct')


class QuestionSerializer(serializers.ModelSerializer):
    """
    This serializer is used to create question and options
    of a exam in the database
    
    Attributes:
        exam_id = used to store the exam_id taken from header
        options = serializer instance for options Model
    """
    
    options = OptionSerializer(many=True)

    class Meta:
        """A class that defines metadata for a Django ModelForm"""
        
        model = academics_models.Question
        fields = ('id', 'text', 'options','mark')

    def create(self, validated_data):
        """
        overriden to create options along with creating questions
        """
        
        options_data = validated_data.pop('options')
        request = self.context.get('request')
        exam_id = request.headers.get('exam_id')
        print(exam_id)
        validated_data['exam'] = \
            academics_models.ExamStandardSubject.objects.get(id=exam_id)
        question = super().create(validated_data)
        
        # create option for question created above 
        for option_data in options_data:
            academics_models.Option.objects.create(
                question=question, **option_data)
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
        """A class that defines metadata for a Django ModelForm"""
        
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
            return Response({"message":"already answered this question"})

        options_data = validated_data.pop('options')
        response =  academics_models.Response.objects.create(student=student)
        
        # removes the [] from options and makes the option int type
        options = [*map(int, options_data[0].strip('[]').split(','))]
        for option in options:
            option = academics_models.Option.objects.get(id=option)
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
            """
            function returns student details and exam result
            """
            
            ret = dict()
            exam_id = instance.id
            student_id = self.context['view'].kwargs.get('student_id')
            exam = academics_models.Exam.objects.get(id=exam_id)
            student = account_models.Student.objects.get(
                user__user__id=student_id)
            
            # set student and exam details
            ret['exam'] = exam.name
            ret['standard'] = exam.classroom.standard
            ret['division'] = exam.classroom.division
            ret['full_name'] = student.user.get_fullname()
            
            questions = academics_models.Question.objects.filter(exam=exam)
            mark = 0
            for question in questions:
                mark = mark + question.mark
            ret['total_mark'] = mark # max mark that can be scored
            
            # find the response of that student and calculate his mark
            responses = academics_models.Response.objects.filter(
                student=student,option__question__exam =exam)
            score =0
            
            for response in responses:
                score = score + response.option.filter(is_correct=True).count()
            ret['score'] = score #mark of the student
            return ret


class AccountSerializer(serializers.ModelSerializer):
    """
    this serializer is used as nested in MarkAttendence
    serializer to print id of the user marking attendence
    """
   
    class Meta:
        """A class that defines metadata for a Django ModelForm"""
        
        model = account_models.Account
        fields = "__all__"


class MarkAttendence(serializers.ModelSerializer):
    """
    Serializer for Attendence model
    """
    
    user  = AccountSerializer(read_only = True)
    is_present = serializers.BooleanField(read_only=True)
    
    class Meta:
        """A class that defines metadata for a Django ModelForm"""
        
        model = academics_models.Attendance
        fields = ["id","user","is_present","date"]

    def create(self, validated_data):
        """
        to set the is_present field true and
        to get the user from authtoken
        """
        
        user = self.context["request"].user.account
        attendence = academics_models.Attendance.objects.create(
            user=user,is_present=True)
        return attendence


