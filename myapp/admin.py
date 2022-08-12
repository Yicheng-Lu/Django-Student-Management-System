import decimal

from django.contrib import admin
from django.db import models
from .models import Topic, Course, Student, Order


# Register your models here.
class CourseInline(admin.TabularInline):
    model = Course
    extra = 0


class TopicAdmin(admin.ModelAdmin):
    inlines = [CourseInline]
    fields = ['name']


class CourseAdmin(admin.ModelAdmin):
    actions = ['course_discount']
    list_display = ['name', 'topic', 'price']
    ordering = ['topic', 'name']

    @admin.action(description='10%% discount')
    def course_discount(self, request, queryset):
        for course in queryset:
            course.price *= decimal.Decimal(0.9)
            course.save()


admin.site.register(Topic, TopicAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student)
admin.site.register(Order)
