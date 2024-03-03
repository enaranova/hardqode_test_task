from product.models import Classroom

def get_classroom(user, course):
    existing_classrooms = Classroom.objects.filter(course=course)

    if existing_classrooms.exists():
        latest_classroom = existing_classrooms.latest('id')

        if latest_classroom.students.count() < course.max_students:
            latest_classroom.students.add(user)
            return f"Enrolled in existing latest classroom ({latest_classroom.name})"
        else:
            new_index = existing_classrooms.count() + 1
            new_classroom_name = f"{course.name} Classroom {new_index}"
            new_classroom = Classroom.objects.create(name=new_classroom_name, course=course)
            new_classroom.students.set([user])
            return f"Enrolled in new classroom ({new_classroom.name})"
    else:
        new_classroom_name = f"{course.name} Classroom 1"
        new_classroom = Classroom.objects.create(name=new_classroom_name, course=course)
        new_classroom.students.set([user])
        return f"Enrolled in new classroom ({new_classroom.name})"
