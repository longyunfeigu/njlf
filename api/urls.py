from django.conf.urls import url, include
from .views.account import LoginView
from .views.course import CourseView

urlpatterns = [
    url('account/login/$', LoginView.as_view(), name='login'),
    url('course/$', CourseView.as_view({'get':'list'}), name='course'),
    url('course/(?P<pk>\d+)/$', CourseView.as_view({'get':'retrieve'}), name='course_detail'),
]
