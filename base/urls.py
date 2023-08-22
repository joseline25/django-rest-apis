from django.urls import path
from .views import *

urlpatterns = [
    path('', endpoints, name='endpoints'),
    path('advocates/', advocate_list, name='advocates'),
    path('advocates/<str:username>/', advocate_details, name='advocate_details'),
]
