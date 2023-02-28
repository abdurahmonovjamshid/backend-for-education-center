from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import (
    CourseSerializer,
    ApplicantSerializer,
    RegisterSerializer,
    GroupSerializer,
    StudentSerializer,
    TeacherSerializer,
    AttendanceSerializer
)
from .models import Course, Applicant, CustomUser, Group, Student, Teacher, Attendance
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView, \
    RetrieveUpdateDestroyAPIView, get_object_or_404
import requests
import json


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


class StudentView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.filter(group=None)
    serializer_class = StudentSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'phone'

    # lookup_field = 'phone'

    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, phone='+' + kwargs['phone'])
        serializer = StudentSerializer(get_object_or_404(Student, phone=user), many=False)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = get_object_or_404(CustomUser, phone='+' + kwargs['phone'])
        serializer = StudentSerializer(get_object_or_404(Student, phone=instance), data=request.data, partial=partial,
                                       many=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

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
        user = get_object_or_404(CustomUser, phone='+' + kwargs['phone'])
        serializer = TeacherSerializer(get_object_or_404(Teacher, phone=user), many=False)
        return Response(serializer.data)


class GroupListView(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAdminUser,)

    def create(self, request, *args, **kwargs):
        try:
            if Group.objects.filter(day=request.data['day'], time=request.data['time'], room=request.data['room']):
                return Response('the room is not empty at this given time', status=400)
        except:
            pass
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GroupView(RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = 'name'

    def update(self, request, *args, **kwargs):
        try:
            if Group.objects.filter(day=request.data['day'], time=request.data['time'], room=request.data['room']):
                return Response('the room is not empty at this given time', status=400)
        except:
            pass
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


# @api_view(['GET', 'POST'])
# def group_attendance(request, name):
#     group = get_object_or_404(Group, name=name)
#     attendance = Attendance.objects.filter(group=group)
#     a = []
#     for n in attendance:
#         serializer = AttendanceSerializer(n, many=False)
#         a.append(serializer.data)
#
#     return Response(a)

class AttendanceView(ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def list(self, request, *args, **kwargs):
        group = get_object_or_404(Group, name=kwargs['name'])
        queryset = Attendance.objects.filter(group=group)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
