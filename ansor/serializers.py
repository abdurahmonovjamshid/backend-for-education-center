from rest_framework import serializers
from .models import Course, Applicant, CustomUser, Teacher, Student, Group, Attendance
from django.contrib.auth.password_validation import validate_password
import json


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('phone', 'password', 'password2', 'first_name', 'last_name', 'is_student', 'is_teacher')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            phone=validated_data['phone'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_student=validated_data['is_student'],
            is_teacher=validated_data['is_teacher'],
        )

        user.set_password(validated_data['password'])
        user.save()

        if validated_data['is_student']:
            student = Student.objects.create(
                phone=user,
                full_name=validated_data['first_name'] + ' ' + validated_data['last_name'],
            )
            student.save()
        else:
            teacher = Teacher.objects.create(
                phone=user,
                full_name=validated_data['first_name'] + ' ' + validated_data['last_name'],
            )
            teacher.save()

        return user


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()
    day = serializers.ChoiceField(choices=['odd', 'even'])

    class Meta:
        model = Group
        fields = ['name', 'teacher', 'room', 'time', 'day', 'course', 'students']

    def to_representation(self, obj):
        teacher = None
        try:
            teacher = obj.teacher.full_name
        except:
            pass

        return {
            "name": obj.name,
            "teacher": teacher,
            "room": obj.room,
            "time": obj.time,
            "day": obj.day,
            "course": obj.course.name,
            "students": [n.full_name for n in obj.student_set.all()],

        }


class StudentSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'group', 'phone', 'balance']

    def to_representation(self, obj):
        group = None
        try:
            group = obj.group.name
        except:
            pass
        return {
            'id': obj.id,
            'full_name': obj.full_name,
            'group': group,
            'phone': obj.phone.phone,
            'balance': obj.balance,
        }


class TeacherSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField(read_only=True)
    phone = serializers.CharField(read_only=True)

    class Meta:
        model = Teacher
        fields = ['id', 'full_name', 'phone', 'groups']

    def get_groups(self, obj):
        return [n.name for n in obj.group_set.all()]


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

    def to_representation(self, obj):
        return {
            'id': obj.id,
            'group': obj.group.name,
            'attended_students': [n['full_name'] for n in StudentSerializer(obj.attended_students, many=True).data],
            'created_at': obj.created_at,

        }
