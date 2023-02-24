from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from .serializers import CourseSerializer, ApplicantSerializer, RegisterSerializer
from .models import Course, Applicant, CustomUser
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
import requests


class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
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
        requests.post(apiURL,
                      json={'chat_id': 872978271, 'text': f'{serializer.data}'})

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
