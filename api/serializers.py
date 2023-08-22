# to convert data into json data
from rest_framework import serializers

from base.models import *


class AdvocateSerializer(serializers.ModelSerializer):
    class  Meta:
        model = Advocate
        fields = '__all__'