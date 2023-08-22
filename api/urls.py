from django.urls import path
from .views import *

urlpatterns = [

    # GET
    path('', hello_world, name='hello_world'),
    path('endpoints/', endpoints, name='endpoints'),
    path('advocates/', advocate_list, name='advocates'),
    path('advocates/<int:id>/', advocate_details, name='advocate_details'),
    # or path('advocates/<str:username>/', advocate_details, name='advocate_details'),
    
    # POST

]
