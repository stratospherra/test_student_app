from django.db import models, migrations
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


def create_unknown_faculty(apps, schema_editor):
    Faculty = apps.get_model('main', 'Faculty')
    Faculty.objects.create(name='Unknown', is_active=True)

class Migration(migrations.Migration):

    dependencies = [
        # добавьте здесь зависимость вашей предыдущей миграции
        ('main', 'название_вашей_последней_миграции'),
    ]

    operations = [
        migrations.RunPython(create_unknown_faculty),
    ]


class Faculty(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Speciality(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.id} {self.last_name} {self.first_name} {self.middle_name}"

    @property
    def formatted_id(self):
        return f"{self.id:06d}"



class Subject(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class StudentStatus(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Notification(models.Model):
    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class ApplicationStatus(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class TypeOfGrades(models.Model):
    title = models.CharField(max_length=255)
    calculate = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    status = models.ForeignKey(StudentStatus, on_delete=models.CASCADE)
    faculties = models.ManyToManyField(Faculty, through='StudentOfFaculty')
    current_faculty = models.ForeignKey(Faculty, related_name='current_students', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.id} {self.last_name} {self.first_name} {self.middle_name}"

    @property
    def formatted_id(self):
        return f"{self.id:06d}"
    
    def calculate_grades(self):
        grades = TypeOfGrades.objects.filter(student=self)
        grades_dict = {grade.grade_type.title: grade.value for grade in grades}

        P1 = (grades_dict.get('ср.т1', 0) + grades_dict.get('рк1', 0)) / 2
        P2 = (grades_dict.get('ср.т2', 0) + grades_dict.get('рк2', 0)) / 2
        OR = (P1 + P2) / 2
        IO = (OR + grades_dict.get('Экзамен', 0)) / 2

        return {
            'P1': P1,
            'P2': P2,
            'OR': OR,
            'IO': IO,
        }
    

class Grade(models.Model):
    id = models.IntegerField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, default=1)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    grade_type = models.ForeignKey(TypeOfGrades, on_delete=models.CASCADE)
    grade = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.student.last_name} - {self.grade_type.title}: {self.subject}"

    @property
    def is_pass(self):
        return self.value >= 50

    @property
    def max_value(self):
        return 100

    @property
    def min_value(self):
        return 0



class StudentOfFaculty(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Student {self.student} in Faculty {self.faculty}"
    

class StudentOfSpeciality(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Student {self.student} in Speciality {self.speciality}"
    

class StudentOfLanguage(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Student {self.student} in Language {self.language}"
    


class DayOfWeek(models.Model):
    # language = models.ForeignKey(Language, on_delete=models.CASCADE)
    name_en = models.CharField(max_length=20)
    name_ru = models.CharField(max_length=20)
    name_kz = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.name_ru + self.name_kz + self.name_en}"


class ScheduleVersion(models.Model):
    version_number = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.version_number


class Schedule(models.Model):
    day_of_week = models.ForeignKey(DayOfWeek, on_delete=models.CASCADE)
    time_start = models.TimeField()
    time_end = models.TimeField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    room = models.CharField(max_length=20)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    version = models.ForeignKey(ScheduleVersion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.day_of_week} {self.time_start}-{self.time_end} {self.subject} ({self.teacher})"
    