from rest_framework import serializers
from product.models import Course, Lesson, Classroom

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = '__all__'

class AvailableCoursesSerializer(serializers.ModelSerializer):
    lesson_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Course
        fields = ['id', 'name', 'start_datetime', 'cost', 'professor', 'min_students', 'max_students', 'lesson_count']
