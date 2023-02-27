from django.contrib.admin import action
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from .serializers import (
    CourseSerializer,
    ApplicantSerializer,
    RegisterSerializer,
    GroupSerializer,
    StudentSerializer,
    TeacherSerializer
)
from .models import Course, Applicant, CustomUser, Group, Student, Teacher
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView, \
    RetrieveUpdateDestroyAPIView, get_object_or_404
import requests


class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = RegisterSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAdminUser,)


class ApplicantView(CreateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.data)

        apiURL = f'https://api.telegram.org/bot5699146037:AAG0b6KHQDUaNU-vIj0y8hYURy6jsZ49U78/sendMessage'
        course = Course.objects.get(pk=serializer.data['course'])
        text = f'''
📝 A new Applicant:

👤 Name: {serializer.data['full_name']};
📚 Course: {course.name};
📞 Phone: {serializer.data['phone']}.
'''
        requests.post(apiURL,
                      json={'chat_id': 872978271, 'text': text})

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class StudentListView(ListAPIView):
    queryset = Student.objects.filter(group=None)
    serializer_class = StudentSerializer
    permission_classes = (IsAdminUser,)


class StudentView(RetrieveUpdateAPIView):
    queryset = Student.objects.filter(group=None)
    serializer_class = StudentSerializer
    permission_classes = (IsAdminUser,)

    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, phone=kwargs['phone'])
        serializer = StudentSerializer(get_object_or_404(Student, phone=user), many=False)
        return Response(serializer.data)


class TeacherListView(ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = (IsAdminUser,)


class TeacherView(RetrieveUpdateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = (IsAdminUser,)

    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, phone=kwargs['phone'])
        serializer = TeacherSerializer(get_object_or_404(Teacher, phone=user), many=False)
        return Response(serializer.data)


class GroupListView(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAdminUser,)


class GroupView(RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'name'
