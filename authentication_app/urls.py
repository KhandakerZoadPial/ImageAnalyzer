from django.urls import path
from .views import *


urlpatterns = [
    path('login', login_, name='login_'),
    path('signup', signup, name='signup'),
    path('verify/<str:code>', verify_account, name='verify_account')
]
