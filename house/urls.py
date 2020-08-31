from django.urls import path
from django.contrib import admin
from .views import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('page/<str:page_name>/', render_page, name='page'),
    path('houseinfo/', Houses.as_view()),
    path('gethousebycode/<str:house_code>/', GetHouseByCode.as_view()),
    path('gethousebyid/<str:id>/', GetHouseByID.as_view()),
    path('updatehouseinfo/<str:id>/', UpdateHouseInfo.as_view()),
    path('search/', SearchHouse.as_view()),
    path('getpostion/', GetPosition.as_view()),
    path('getplot/', GetPlot.as_view()),
    path('gethousebysort/', GetHouseBySort.as_view()),
    path('gethousebyplot/', GetHouseByPlot.as_view()),
    path('getdealdata/', GetDealData.as_view()),
    path('validatehousecode/', ValidateHouseCode.as_view()),
]
