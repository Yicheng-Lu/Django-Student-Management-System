import json

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone

from .forms import OrderForm, InterestForm, LoginForm
from .models import Topic, Course, Student, Order


def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    if 'last_login' not in request.session:
        return HttpResponse('Your last login was more than one hour ago')
    last_login = request.session['last_login']
    return render(request, r'myapp/index.html', {'top_list': top_list, 'last_login': last_login})


def about(request):
    count = request.session.get('about_visits', 0)
    request.session['about_visits'] = count + 1
    request.session.set_expiry(300)
    return render(request, r'myapp/about.html', {'about_visits': count})


def detail(request, topic_no):
    topic = get_object_or_404(Topic, id=topic_no)
    cour_list = Course.objects.filter(topic=topic_no)
    return render(request, r'myapp/detail.html', {'top_detail': topic, 'cou_list': cour_list})


def courses(request):
    cour_list = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'cour_list': cour_list})


def place_order(request):
    msg = ''
    courlist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.levels <= order.course.stages:
                price = order.course.price
                if price >= 150:
                    order.order_price = order.course.discount()
                order.save()
                msg = 'Your course has been ordered successfully.'
            else:
                msg = 'You exceeded the number of levels for this course.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/place_order.html', {'order_form':form, 'msg':msg, 'courlist':courlist})


def course_detail(request, course_no):
    course = get_object_or_404(Course, id=course_no)
    if request.method == "POST":
        form = InterestForm(request.POST)
        if form.is_valid():
            course.interested = course.interested+1
            course.save()
            return courses(request)
    else:
        form = InterestForm()
    return render(request, 'myapp/course_detail.html', {'form': form, 'course': course})


@login_required
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            json_str = json.dumps({'created_at': timezone.localtime(timezone.now())}, default=str)
            request.session['last_login'] = json_str
            request.session.set_expiry(3600)
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html', {'loginForm': LoginForm})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))


@login_required
def myaccount(request):
    usr = request.user
    if Student.objects.get(username=usr.username):
        order_list = Order.objects.filter(student=usr)
        topic_list = Topic.objects.filter(student=usr)
        course_list = list()
        course_name = [order.course.name for order in order_list]
        for name in course_name:
            if name not in course_list:
                course_list.append(name)
        return render(request, 'myapp/myaccount.html', {'firstName': usr.first_name,
                                                        'lastName': usr.last_name,
                                                        'course_list': course_list,
                                                        'topic_list': topic_list})
    else:
        msg = 'You are not a registered student.'
        return render(request, 'myapp/order_response.html', {'msg': msg})


def testCookie(request):
    if request.method == "GET":
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            return HttpResponse("Cookie available")
        else:
            request.session.set_test_cookie()
            return HttpResponse("Please enable cookies")
    return render(request, 'myapp/index.html')