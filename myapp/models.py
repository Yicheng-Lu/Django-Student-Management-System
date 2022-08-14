from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
import datetime

def validate_price(value):
    if value < 50 or value > 500:
        raise ValidationError(
            ('Price musb be between 50 and 500.'),
            params={'value': value},
        )


class Topic(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Course(models.Model):
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_price])
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    interested = models.PositiveIntegerField(default=0)
    stages = models.PositiveIntegerField(default=3)

    def __str__(self):
        return self.name

    def discount(self):
        return float(self.price) * 0.9


class Student(User):
    CITY_CHOICES = [('WS', 'Windsor'),
                    ('CG', 'Calgary'),
                    ('MR', 'Montreal'),
                    ('VC', 'Vancouver')]
    school = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=50, blank=True, )
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    interested_in = models.ManyToManyField(Topic)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Order(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='orders')
    levels = models.PositiveIntegerField()
    ORDER_CHOICES = [(0, 'Cancelled'), (1, 'Order Confirmed')]
    order_status = models.IntegerField(choices=ORDER_CHOICES, default=1)
    order_date = models.DateField()
    order_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @classmethod
    def total_cost(self):
        return self.course.price

    def __str__(self):
        return self.course.name + " by " + self.student.username

