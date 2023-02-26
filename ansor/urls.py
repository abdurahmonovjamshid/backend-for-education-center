from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register('courses', views.CourseViewSet)

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('', include(router.urls)),

    path('applicant/', views.ApplicantView.as_view()),

    path('group/', views.GroupListView.as_view()),
    path('group/<str:name>', views.GroupView.as_view()),

    path('student/', views.StudentListView.as_view()),
    path('student/<str:phone>', views.StudentView.as_view()),
]
