from django.urls import path
from .views import *

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('signup/', SignUp.as_view(), name='signup'),

    path('add-course/', AddCourse.as_view(), name='add-course'),
    path('add-lesson/', AddLesson.as_view(), name='add-lesson'),

    path('view-lessons/', ViewLessons.as_view(), name='view-lessons'),
    path('available-courses/', AvailableCourses.as_view(), name='available-courses'),
    path('enroll-user/', EnrollUser.as_view(), name='enroll-user'),
    path('balance-classrooms/', BalanceClassrooms.as_view(), name = 'balance-classrooms'),

    path('view-classrooms/', ViewClassrooms.as_view(), name='view-classrooms'),
]