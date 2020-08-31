from rest_framework_mongoengine import serializers
from .models import *


class HouseSInfoSerializers(serializers.DocumentSerializer):
    class Meta:
        model = HouseInfo
        fields = ['id', 'title', 'imgs', 'bedroom', 'area', 'floor', 'year',\
                  'plot', 'position', 'total_price', 'unit_price']


class HouseInfoSerializers(serializers.DocumentSerializer):

    class Meta:
        model = HouseInfo
        fields = '__all__'


class PlotInfoSerializers(serializers.DocumentSerializer):
    class Meta:
        model = HouseInfo
        fields = ['plot', 'imgs','year', 'position', 'unit_price']