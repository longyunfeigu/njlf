from django.conf.urls import url, include
from .views.account import LoginView

urlpatterns = [
    url('account/login/$', LoginView.as_view(), name='login')
]
