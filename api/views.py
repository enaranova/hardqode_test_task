from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from product.models import Course, Lesson, Classroom
from .serializers import CourseSerializer, LessonSerializer, ClassroomSerializer, AvailableCoursesSerializer
from django.db.models import Count
from django.utils import timezone
from .permissions import IsProfessor, IsStudent
from django.contrib.auth.models import User, Group
from .utils import get_classroom

class SignUp(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response("Username and password are required", status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response("Username already taken", status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)

        return Response("User registered successfully", status=status.HTTP_201_CREATED)

class Login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response("User logged in")
        else:
            return Response("Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)

class Logout(APIView):
    def post(self, request):
        logout(request)
        return Response("User logged out")

class AvailableCourses(APIView):
    def get(self, request):
        current_datetime = timezone.now()
        available_courses = Course.objects.filter(start_datetime__gt=current_datetime).annotate(lesson_count=Count('lesson'))
        serializer = AvailableCoursesSerializer(available_courses, many=True)
        return Response(serializer.data)

class AddCourse(APIView):
    permission_classes = [IsProfessor]

    def post(self, request):
        name = request.data.get('name')
        start_datetime = request.data.get('start_datetime')
        cost = request.data.get('cost')
        professor_username = request.data.get('professor')
        min_students = request.data.get('min_students')
        max_students = request.data.get('max_students')

        try:
            professor = User.objects.get(username=professor_username)
        except User.DoesNotExist:
            return Response("No such professor", status=status.HTTP_404_NOT_FOUND)

        course = Course.objects.create(
            name=name,
            start_datetime=start_datetime,
            cost=cost,
            professor=professor,
            min_students=min_students,
            max_students=max_students
        )

        return Response("Course created successfully", status=status.HTTP_201_CREATED)
    
class AddLesson(APIView):
    permission_classes = [IsProfessor]
    def post(self, request):
        name = request.data.get('name')
        video_url = request.data.get('video_url')
        course_name = request.data.get('course')

        try:
            course = Course.objects.get(name=course_name)
        except Course.DoesNotExist:
            return Response("No such course", status=status.HTTP_404_NOT_FOUND)

        lesson = Lesson.objects.create(
            name=name,
            video_url=video_url,
            course=course
        )

        return Response("Lesson created successfully", status=status.HTTP_201_CREATED)
    
class ViewLessons(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        user = self.request.user
        lessons = Lesson.objects.filter(course__classroom__students=user)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

class EnrollUser(APIView):
    # permission_classes = [IsAdminUser]

    def post(self, request):
        username = request.data.get('username')
        course_name = request.data.get('course_name')

        try:
            user = User.objects.get(username=username)
        except Course.DoesNotExist:
            return Response("No such user", status=status.HTTP_404_NOT_FOUND)
        
        try:
            course = Course.objects.get(name=course_name)
        except Course.DoesNotExist:
            return Response("No such course", status=status.HTTP_404_NOT_FOUND)
        
        response_message = get_classroom(user, course)

        students_group = Group.objects.get(name='Students')
        # добавляем юзера в группу с правами доступа "Students"
        user.groups.add(students_group)

        return Response(response_message, status=status.HTTP_200_OK)

class BalanceClassrooms(APIView):
    def post(self, request):
        course_name = request.data.get('course_name')

        try:
            course = Course.objects.get(name=course_name)
        except Course.DoesNotExist:
            return Response(f"No such course: {course_name}", status=status.HTTP_404_NOT_FOUND)
        
        course_classrooms = Classroom.objects.filter(course=course).order_by('-id')

        number_of_classrooms = len(course_classrooms)

        latest_classroom = course_classrooms[0]
        classrooms_to_divide = course_classrooms[1:]

        latest_classroom_students_count = latest_classroom.students.count()

        # проверка общее количество студентов достаточно для минимальных групп
        if latest_classroom_students_count + (course.max_students * (number_of_classrooms - 1)) < course.min_students * number_of_classrooms:
            return Response("Classrooms can't be balanced - not enough students")

        students_to_distribute_general = course.max_students - latest_classroom_students_count
        students_to_distribute_per_classroom = students_to_distribute_general // number_of_classrooms

        # Перемещаем студентов в класс с последним id
        for classroom in classrooms_to_divide:
            students_to_move = min(students_to_distribute_per_classroom, classroom.students.count())
            latest_classroom.students.add(*classroom.students.all()[:students_to_move])
            classroom.students.remove(*classroom.students.all()[:students_to_move])

        return Response("Classrooms balanced successfully", status=status.HTTP_200_OK)

class ViewClassrooms(APIView):
    # permission_classes = [IsProfessor]

    def get(self, request):
        classrooms = Classroom.objects.all()
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(serializer.data)
    