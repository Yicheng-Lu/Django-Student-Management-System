from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from .models import Topic, Course, Student, Order


def index(request):
    cou_list = Course.objects.all().order_by('price')[::-1]
    response = HttpResponse()
    heading1 = '<p>' + 'List of courses: ' + '</p>'
    response.write(heading1)
    for course in cou_list[:5]:
        if course.for_everyone:
            para = '<p>' + str(course.name) + ': ' + str(course.price) \
                   + '&nbsp;&nbsp;&nbsp;&nbsp;This Course is For Everyone!' + '</p>'
        else:
            para = '<p>' + str(course.name) + ': ' + str(course.price) \
                   + '&nbsp;&nbsp;&nbsp;&nbsp;This Course is Not For Everyone!' + '</p>'
        response.write(para)
    return response


# def index(request):
#     top_list = Topic.objects.all().order_by('id')[:10]
#     return render(request, r'myapp/index0.html', {'top_list': top_list})


def about(request):
    response = HttpResponse()
    response.write('<p>This is an E-learning Website! Search our Topics to find all available Courses.</p>')
    return response


# def about(request):
#     return render(request, r'myapp/about0.html')


def detail(request, top_no):
    # try:
    #     Topic.objects.get(id=top_no)
    # except Topic.DoesNotExist:
    #     raise Http404("No Topic matches the id!")
    obj = get_object_or_404(Topic, id=top_no)
    response = HttpResponse()
    response.write('<p>' + obj.name + '</p>')
    return response


# def detail(request, top_no):
#     try:
#         Topic.objects.get(id=top_no)
#     except Topic.DoesNotExist:
#         raise Http404("No Topic matches the id!")
#     topic = Topic.objects.get(id=top_no)
#     cou_list = Course.objects.filter(topic=top_no)
#     return render(request, r'myapp/detail0.html', {'top_detail': topic, 'cou_list': cou_list})