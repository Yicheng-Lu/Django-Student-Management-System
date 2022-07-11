from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render

from .forms import OrderForm
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
                order.save()
                msg = 'Your course has been ordered successfully.'
            else:
                msg = 'You exceeded the number of levels for this course.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/place_order.html', {'order_form':form, 'msg':msg, 'courlist':courlist})


def course_detail(request, course_no):
    course = Course.objects.get(course_no)
    return render(request, 'myapp/course_detail.html', {'course': course})
