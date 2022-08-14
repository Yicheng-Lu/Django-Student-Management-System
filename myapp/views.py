import json

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.utils import timezone

from .forms import OrderForm, InterestForm, LoginForm, RegisterForm
from .models import Topic, Course, Student, Order


def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    # if 'last_login' not in request.session:
    #     return HttpResponse('Your last login was more than one hour ago')
    # last_login = request.session['last_login']
    return render(request, r'myapp/index.html', {'top_list': top_list})  # , 'last_login': last_login})


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
    return render(request, 'myapp/place_order.html', {'order_form': form, 'msg': msg, 'courlist': courlist})


def course_detail(request, course_no):
    course = get_object_or_404(Course, id=course_no)
    if request.method == "POST":
        form = InterestForm(request.POST)
        if form.is_valid():
            course.interested = course.interested + 1
            course.save()
            return courses(request)
    else:
        form = InterestForm()
    return render(request, 'myapp/course_detail.html', {'form': form, 'course': course})


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


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myapp:login')
    else:
        form = RegisterForm
    return render(request, 'myapp/register.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))


@login_required(login_url='/myapp/login')
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


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "myapp/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="myapp/password_reset.html",
                  context={"password_reset_form": password_reset_form})


def testCookie(request):
    if request.method == "GET":
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            return HttpResponse("Cookie available")
        else:
            request.session.set_test_cookie()
            return HttpResponse("Please enable cookies")
    return render(request, 'myapp/index.html')


@login_required(login_url='/myapp/login')
def myorders(request):
    usr = request.user
    if Student.objects.get(username=usr.username):
        order_list = Order.objects.filter(student=usr)
        return render(request, 'myapp/myorders.html', {'order_list': order_list})
    else:
        msg = 'You are not a registered student.'
        return render(request, 'myapp/order_response.html', {'msg': msg})


def profile_upload(request):
    return render(request, 'myapp/profile_upload.html')

