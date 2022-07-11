from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render

from .forms import OrderForm, InterestForm
from .models import Topic, Course, Student, Order


def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, r'myapp/index.html', {'top_list': top_list})


def about(request):
    return render(request, r'myapp/about.html')


def detail(request, topic_no):
    topic = get_object_or_404(Topic, id=topic_no)
    cou_list = Course.objects.filter(topic=topic_no)
    return render(request, r'myapp/detail.html', {'top_detail': topic, 'cou_list': cou_list})


def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'courlist': courlist})


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
    return render(request, 'Myapp/course_detail.html', {'form': form, 'cur': course})
