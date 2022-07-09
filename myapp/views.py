from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from .models import Topic, Course, Student, Order


def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, r'myapp/index.html', {'top_list': top_list})


def about(request):
    return render(request, r'myapp/about.html')


def detail(request, top_no):
    topic = get_object_or_404(Topic, id=top_no)
    cou_list = Course.objects.filter(topic=top_no)
    return render(request, r'myapp/detail.html', {'top_detail': topic, 'cou_list': cou_list})

def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'courlist': courlist})