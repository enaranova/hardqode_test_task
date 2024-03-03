from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    professor = models.ForeignKey(User, on_delete=models.CASCADE)
    min_students = models.IntegerField()
    max_students = models.IntegerField()

class Lesson(models.Model):
    name = models.CharField(max_length=255)
    video_url = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Classroom(models.Model):
    name = models.CharField(max_length=255)
    students = models.ManyToManyField(User)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
