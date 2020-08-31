import json, datetime, time, os
from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework_mongoengine import generics
from .serializers import *
from house.serializers import HouseInfoSerializers, HouseSInfoSerializers
from house.models import HouseInfo


class Register(generics.CreateAPIView):
    queryset = User.objects.all(), Publications.objects.all(), UserInfo.objects.all()
    serializer_class = UserSerializers, SubscriptionSerializers, UserInfoSerializers

    def post(self, request, *args, **kwargs):
        user = User.objects.create(username=request.POST.get('name'), password=request.POST.get('password'), tel=request.POST.get('tel'))
        print(user)
        Publications.objects.create(tel=request.POST.get('tel'), publist=[])
        UserInfo.objects.create(tel=request.POST.get('tel'), username=request.POST.get('name'))
        request.session['user'] = user.username
        return Response({'status': 200}, status=200)


class ValidateUsername(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def get(self, request, *args, **kwargs):
        try:
            User.objects.get(username=request.GET.get('name'))
        except:
            return Response(json.dumps({'status': 200, 'msg': '用户名可用'}))
        else:
            return Response(json.dumps({'status': 405, 'msg': '用户名已存在'}))


class Login(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.GET.get('username'))
        except:
            return Response(json.dumps({'status': 405, 'msg': '用户名或密码错误'}))
        else:
            password = request.GET.get('password')
            if user.password == password:
                request.session['user'] = user.username
                return Response(json.dumps({'status': 200, 'msg': '登陆成功'}))
            else:
                return Response(json.dumps({'status': 405, 'msg': '用户名或密码错误'}))


class OneUser(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    lookup_field = 'name'

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=kwargs.get('name'))
        except:
            return Response(json.dumps({'status': 405, 'msg': '用户名信息不存在'}))
        else:
            tel = user.tel[:3]+'****'+user.tel[7:]
            password = '*'*len(user.password)
            return Response(json.dumps({'status': 405, 'msg': '用户名信息不存在', 'tel': tel, 'password': password}))

    def put(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=kwargs.get('name'))
        except:
            return Response(json.dumps({'status': 405, 'msg': '用户名信息不存在'}))
        else:
            if request.POST.get('old_password') == user.password:
                user.password = request.POST.get('new_password')
                user.save()
                return Response(json.dumps({'status': 200, 'msg': '修改成功'}))
            else:
                return Response(json.dumps({'status': 400, 'msg': '原密码错误'}))


def logout(request):
    del request.session['user']
    return HttpResponse(status=200)


def getlog(request):
    return HttpResponse(request.session['user'], status=200)


class OneUserInfo(generics.RetrieveUpdateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializers
    lookup_field = 'username'


# 用户上传房屋信息
class PublishHouse(generics.CreateAPIView):
    queryset = HouseInfo.objects.all(), Publications.objects.all()
    serializer_class = HouseInfoSerializers, SubscriptionSerializers

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=request.session.get('user'))
        userPublications = Publications.objects.get(tel=user.tel)
        try:
            HouseInfo.objects.create(
                title=request.POST.get('title'),
                imgs=request.POST.get('imgs').split('-')[1:],
                bedroom=[request.POST.get('type1'), request.POST.get('type2')],
                area=request.POST.get('area'),
                total_price=request.POST.get('total_price'),
                plot=request.POST.get('plot'),
                type=[request.POST.get('type1')+'室', request.POST.get('type2')+'厅', request.POST.get('type3')+'卫'],
                unit_price=str(int(float(request.POST.get('total_price'))/float(request.POST.get('area'))*10000)),
                position=[request.POST.get('position1'), request.POST.get('position2'), request.POST.get('position3')],
                down_payment=request.POST.get('down_payment'),
                year=request.POST.get('year'),
                direction=request.POST.get('direction'),
                house_type=request.POST.get('house_type'),
                floor=request.POST.get('floor'),
                decoration=request.POST.get('decoration'),
                property_year=request.POST.get('property_year'),
                elevator=request.POST.get('elevator'),
                house_year=request.POST.get('house_year'),
                property=request.POST.get('property'),
                heating=request.POST.get('heating'),
                only=request.POST.get('only'),
                one_hand=request.POST.get('one_hand'),
                core_point=request.POST.get('core_point'),
                owner_men=request.POST.get('owner_men'),
                service_introduction=request.POST.get('service_introduction'),
                house_code=request.POST.get('house_code'),
                add_date="{}年{}月{}日".format(str(datetime.datetime.now().year), str(datetime.datetime.now().month), str(datetime.datetime.now().day)),
                the_host=request.session.get('user'),
            )
            userPublications.publist.append(request.POST.get('house_code'))
            userPublications.save()
        except Exception as e:
            print(e)
            return Response(json.dumps({'status': 501, 'msg': '发布失败'}))
        else:
            return Response(json.dumps({'status': 200, 'msg': '发布成功'}))


# 获取用户上传房屋信息
class GetUserPub(generics.ListAPIView):
    # queryset = HouseInfo.objects.all()
    serializer_class = HouseSInfoSerializers

    def get(self, request, *args, **kwargs):
        try:
            houses = HouseInfo.objects.filter(the_host=request.session.get('user'))
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


# 图片上传
def uploadPic(request):
    # 初始化将要返回的数据
    print('--------------------------------------')
    obj = dict()
    if request.method == 'POST':
        files = request.FILES.getlist('imgs', None)
        if not files:
            return HttpResponse(json.dumps({'status': 404, 'msg': '没有上传的文件'}))
        else:
            dirs = '/images/house_img'
            try:
                for file in files:
                    t = time.time()     #PS：注释中的是上传文件中的另一种方法哦。各自选用
                    suffix = os.path.splitext(file.name)[0]
                    path = dirs + 'banner' + str(int(round(t * 1000))) + suffix #毫秒级时间戳
                    with open(path, 'wb') as f:
                        for line in file.chunks():
                            f.write(line)
                    return HttpResponse(json.dumps({'status': 200, 'msg': '上传成功'}))
            except Exception as e:
                obj['error'] = e
                return HttpResponse(json.dumps({'status': 404, 'msg': '上传失败'}))
    return HttpResponse(json.dumps({'status': 404, 'msg': '上传失败'}))


def render_page(request, page_name):
    return render(request, '{}'.format(page_name))