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
    path(r'password_reset', views.password_reset_request, name="password_reset"),
    path(r'register', views.user_register, name='register'),
    path(r'myorders', views.myorders, name='myorders'),
    path(r'profile_upload_page', views.profile_upload_page, name='profile_upload_page'),
    path(r'profile_upload_handler', views.profile_upload_handler, name='profile_upload_handler'),
    path(r'request_profile/<int:student_id>', views.profile_request_controller, name='request_profile'),

]
