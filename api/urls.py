from django.conf.urls import url, include
from .views.account import LoginView
from .views.course import CourseView
from .views.news import NewsView

urlpatterns = [
    url('account/login/$', LoginView.as_view(), name='login'),
    url('course/$', CourseView.as_view({'get':'list'}), name='course'),
    url('course/(?P<pk>\d+)/$', CourseView.as_view({'get':'retrieve'}), name='course_detail'),
    url('news/$', NewsView.as_view({'get':'list'}), name='news'),
    url('news/(?P<pk>\d+)/$', NewsView.as_view({'get':'retrieve'}), name='news_detail'),
]
