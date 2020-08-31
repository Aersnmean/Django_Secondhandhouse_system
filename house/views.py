import json
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django_filters import rest_framework

# 首页
def index(request):
    return render(request, 'index.html')


# 页面渲染
def render_page(request, page_name):
    return render(request, '{}'.format(page_name))


# 获取二手房信息
class Houses(generics.ListAPIView):
    queryset = HouseInfo.objects.all()
    serializer_class = HouseSInfoSerializers

    def get(self, request, *args, **kwargs):
        try:
            houses = HouseInfo.objects.all()
        except Exception as e:
            print(e)
            return Response({'status': 404, 'msg': '找不到该房屋信息'})
        else:
            page = self.paginate_queryset(houses)
            total = self._paginator.count
            if page is not None:
                house_list = self.get_serializer(page, many=True).data
                return_dict = {
                    'total': total,
                    'limit': 20,
                    'list': house_list
                }
                return Response(return_dict, status=200)


# 根据房屋编号查找
class GetHouseByCode(generics.RetrieveAPIView):
    queryset = HouseInfo.objects.all()
    serializer_class = HouseInfoSerializers
    lookup_field = 'house_code'


# 根据房屋ID查找
class GetHouseByID(generics.RetrieveUpdateDestroyAPIView):
    queryset = HouseInfo.objects.all()
    serializer_class = HouseInfoSerializers
    lookup_field = 'id'


class UpdateHouseInfo(generics.CreateAPIView):
    queryset = HouseInfo.objects.all()
    serializer_class = HouseInfoSerializers

    def post(self, request, *args, **kwargs):
        house = HouseInfo.objects.get(id=kwargs.get('id'))
        house.title=request.POST.get('title')
        house.bedroom=[request.POST.get('type1'), request.POST.get('type2')]
        house.area=request.POST.get('area')
        house.total_price=float(request.POST.get('total_price'))
        house.plot=request.POST.get('plot')
        house.type=[request.POST.get('type1') + '室', request.POST.get('type2') + '厅', request.POST.get('type3') + '卫']
        house.unit_price=int(float(request.POST.get('total_price')) / float(request.POST.get('area')) * 10000)
        house.position=[request.POST.get('position1'), request.POST.get('position2'), request.POST.get('position3')]
        house.down_payment=request.POST.get('down_payment')
        house.year=request.POST.get('year')
        house.direction=request.POST.get('direction')
        house.house_type=request.POST.get('house_type')
        house.floor=request.POST.get('floor')
        house.decoration=request.POST.get('decoration')
        house.property_year=request.POST.get('property_year')
        house.elevator=request.POST.get('elevator')
        house.house_year=request.POST.get('house_year')
        house.property=request.POST.get('property')
        house.heating=request.POST.get('heating')
        house.only=request.POST.get('only')
        house.one_hand=request.POST.get('one_hand')
        house.core_point=request.POST.get('core_point')
        house.owner_men=request.POST.get('owner_men')
        house.service_introduction=request.POST.get('service_introduction')
        house.house_code=request.POST.get('house_code')
        house.the_host=request.session.get('user')
        house.save()
        return Response({'status': 200, 'msg': '修改成功'})


# 根据分类查找
class GetHouseBySort(generics.ListAPIView):
    queryset = HouseInfo.objects.all()
    serializer_class = HouseSInfoSerializers

    def get(self, request, *args, **kwargs):
        pos_sort = request.GET.get('区域：')
        pri_sort = request.GET.get('售价：').split('-')
        area_sort = request.GET.get('面积：').split('-')
        bed_sort = request.GET.get('房型：')
        # print(pos_sort, pri_sort, area_sort, bed_sort)
        try:
            houses = list(HouseInfo.objects.all())
            if pos_sort != '全部':
                for house in houses[:]:
                    if pos_sort != house.position[0]:
                        houses.remove(house)
            if pri_sort[0] != '全部':
                for house in houses[:]:
                    price = float(house.total_price)
                    if len(pri_sort) == 1:
                        if pri_sort[0][-1] == '下':
                            if price >= int(pri_sort[0][:-3]):
                                houses.remove(house)
                        else:
                            if price <= int(pri_sort[0][:-3]):
                                houses.remove(house)
                    else:
                        if (price <= int(pri_sort[0])) or (price >= int(pri_sort[1][:-1])):
                            houses.remove(house)
            if area_sort[0] != '全部':
                for house in houses[:]:
                    area = float(house.area)
                    if len(area_sort) == 1:
                        if pri_sort[0][-1] == '下':
                            if area >= int(area_sort[0][:-2]):
                                houses.remove(house)
                        else:
                            if area <= int(area_sort[0][:-2]):
                                houses.remove(house)
                    else:
                        if (area <= int(area_sort[0])) or (area >= int(area_sort[1][:-2])):
                            houses.remove(house)
            if bed_sort != '全部':
                if bed_sort == '一室':
                    for house in houses[:]:
                        if house.bedroom[0] != '1':
                            houses.remove(house)
                elif bed_sort == '两室':
                    for house in houses[:]:
                        if house.bedroom[0] != '2':
                            houses.remove(house)
                elif bed_sort == '三室':
                    for house in houses[:]:
                        if house.bedroom[0] != '3':
                            houses.remove(house)
                elif bed_sort == '四室':
                    for house in houses[:]:
                        if house.bedroom[0] != '4':
                            houses.remove(house)
                elif bed_sort == '五室':
                    for house in houses[:]:
                        if house.bedroom[0] != '5':
                            houses.remove(house)
                else:
                    for house in houses[:]:
                        if int(house.bedroom[0]) <= 5:
                            houses.remove(house)
        except Exception as e:
            print(e)
            return Response({'status': 404, 'msg': '找不到该房屋信息'})
        else:
            page = self.paginate_queryset(houses)
            total = self._paginator.count
            if page is not None:
                house_list = self.get_serializer(page, many=True).data
                return_dict = {
                    'total': total,
                    'limit': 20,
                    'list': house_list
                }
                return Response(return_dict, status=200)
            # ser = HouseSInfoSerializers(houses, many=True)
            # return Response(ser.data, status=200)


# 搜索
class SearchHouse(generics.ListAPIView):
    queryset = HouseInfo.objects.all()
    serializer_class = HouseSInfoSerializers

    def get(self, request, *args, **kwargs):
        try:
            houses = HouseInfo.objects.filter(title__contains=request.GET.get('kw'))
        except Exception as e:
            print(e)
            return Response({'status': 404, 'msg': '找不到该房屋信息'})
        else:
            page = self.paginate_queryset(houses)
            total = self._paginator.count
            if page is not None:
                house_list = self.get_serializer(page, many=True).data
                return_dict = {
                    'total': total,
                    'limit': 20,
                    'list': house_list
                }
                return Response(return_dict, status=200)


# 获取区域信息
class GetPosition(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        houses = HouseInfo.objects.all()
        position = list()
        for house in houses:
            if house.position[0] not in position:
                position.append(house.position[0])
        return Response({'data': position}, status=200)


# 获取小区信息
class GetPlot(generics.ListAPIView):
    serializer_class = PlotInfoSerializers

    def get(self, request, *args, **kwargs):
        try:
            houses = HouseInfo.objects.all()
            plots = []
            for house in houses:
                if house.plot not in plots:
                    plots.append(house.plot)
            houses = []
            for plot in plots:
                house = HouseInfo.objects.filter(plot=plot)[0]
                houses.append(house)
        except Exception as e:
            print(e)
            return Response({'status': 404, 'msg': '找不到小区信息'})
        else:
            page = self.paginate_queryset(houses)
            total = self._paginator.count
            if page is not None:
                house_list = self.get_serializer(page, many=True).data
                return_dict = {
                    'total': total,
                    'limit': 20,
                    'list': house_list
                }
                return Response(return_dict, status=200)


class GetHouseByPlot(generics.ListAPIView):
    queryset = HouseInfo.objects.all()
    serializer_class = HouseSInfoSerializers

    def get(self, request, *args, **kwargs):
        try:
            plot = request.GET.get('plot')
            houses = HouseInfo.objects.filter(plot=plot)
        except Exception as e:
            print(e)
            return Response({'status': 404, 'msg': '找不到房屋信息'})
        else:
            page = self.paginate_queryset(houses)
            total = self._paginator.count
            if page is not None:
                house_list = self.get_serializer(page, many=True).data
                return_dict = {
                    'total': total,
                    'limit': 20,
                    'list': house_list
                }
                return Response(return_dict, status=200)


# 获取交易数据
class GetDealData(generics.ListCreateAPIView):
    queryset = HouseInfo.objects.all()
    serializer_class = HouseSInfoSerializers

    def get(self, request, *args, **kwargs):
        date = []
        num = []
        with open('common_static/txt/deal_data.txt', 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip('\n').split('\t')
                num.append(int(line[1])//10)
                date.append(line[0].split('T')[0][5:])
        return Response({'date': date, 'num': num}, status=200)

    def post(self, request, *args, **kwargs):
        date = []
        num = []
        with open('common_static/txt/deal_data.txt', 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip('\n').split('\t')
                num.append(int(line[1]) // 10)
                date.append(line[0].split('T')[0])
        return Response({'date': date, 'num': num}, status=200)


class ValidateHouseCode(generics.RetrieveAPIView):
    queryset = HouseInfo.objects.all()
    serializer_class = HouseSInfoSerializers

    def get(self, request, *args, **kwargs):
        try:
            HouseInfo.objects.get(house_code=request.GET.get('house_code'))
        except:
            return Response(json.dumps({'status': 200, 'msg': '房屋编码可用'}))
        else:
            return Response(json.dumps({'status': 405, 'msg': '房屋编码已存在'}))