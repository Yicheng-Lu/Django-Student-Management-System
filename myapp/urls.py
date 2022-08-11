from django.urls import path
from myapp import views

app_name = 'myapp'
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about', views.about, name='about'),
    path(r'<int:topic_no>', views.detail, name='detail'),
    path(r'courses', views.courses, name='courses'),
    path(r'placeorder', views.place_order, name='place_order'),
    path(r'courses/<int:course_no>', views.course_detail, name="course_detail"),
    path(r'login', views.user_login, name='login'),
    path(r'logout', views.user_logout, name='logout'),
    path(r'myaccount', views.myaccount, name='myaccount'),
    path(r'testCookie', views.testCookie, name='testCookie'),
]