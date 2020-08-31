from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('page/<str:page_name>/', render_page, name='page'),
    path('reg/', Register.as_view()),
    path('log/', Login.as_view()),
    path('logout/', logout),
    path('oneuser/<name>/', OneUser.as_view()),
    path('validate_username/', ValidateUsername.as_view()),
    path('publish/', PublishHouse.as_view()),
    path('getuserpub/', GetUserPub.as_view()),
    path('userinfo/<username>/', OneUserInfo().as_view()),
    path('uploadimg/', uploadPic),
    path('getlog/', getlog)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
