from django.urls import path
from .views import *

# for authentication
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # for Advocate
    # GET
    path('', hello_world, name='hello_world'),
    path('endpoints/', endpoints, name='endpoints'),
    path('advocates/', advocate_list, name='advocates'),
    # path('advocates/<int:id>/', advocate_details, name='advocate_details'),
    # or path('advocates/<str:username>/', advocate_details, name='advocate_details'),

    # POST
    # for class based views, the urls are
    path('advocates/<int:id>/', AdvocateDetails.as_view(),
         name='advocate_details_class'),


    # for Company
    path('companies/', companies_list, name='companies_list'),
    path('companies/<int:id>/', CompanyDetails.as_view(),
         name='company_details_class'),
    
    # for authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
