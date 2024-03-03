from django.contrib import admin
from .models import Course, Lesson, Classroom

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'start_datetime', 'cost', 'professor', 'min_students', 'max_students']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'video_url', 'course']

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'display_students', 'course']

    def display_students(self, obj):
        return ", ".join([str(student) for student in obj.students.all()])
    
    display_students.short_description = 'Студенты'
