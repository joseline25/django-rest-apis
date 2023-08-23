# to convert data into json data
from rest_framework import serializers

from base.models import *


class CompanySerializer(serializers.ModelSerializer):
    #display the number of employees of a company
    employee_count = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Company
        fields = '__all__'

    # get the number of employees of a company
    # note that the name of the function is get_ + the name of the new field: employee_count !!!!
    # self refer to the serialiser and obj, to the model
    def get_employee_count(self, obj):
        count = obj.advocate_set.count() 
        # note the advocate_set to get all the advocates
        #this line above does the job!!  and assign to count, the number of advocates
        # related to this particular company
        return count

class AdvocateSerializer(serializers.ModelSerializer):
    # since there is the field company in the Advocate model,
    # we can get all the value of the company object
    company = CompanySerializer()

    class Meta:
        model = Advocate
        fields = ['username', 'bio', 'company']
