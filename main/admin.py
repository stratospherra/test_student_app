# from django.contrib import admin
# from .models import (
#     Faculty, Speciality, Language, News, Notification,
#     Application, Student, Grade, Instructor, Course, Discipline
# )

# class StudentInline(admin.TabularInline):  
#     model = Student
#     extra = 1

# class GradeInline(admin.TabularInline):  
#     model = Grade
#     extra = 1

# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('formatted_id', 'last_name', 'first_name', 'middle_name', 'date_of_birth', 'email', 'faculty', 'speciality', 'course')

#     def formatted_id(self, obj):
#         return f"{obj.id:06d}"

#     formatted_id.short_description = 'ID'

# @admin.register(Grade)
# class GradeAdmin(admin.ModelAdmin):
#     list_display = ('student', 'course', 'instructor', 'grade_value')

# @admin.register(Faculty)
# class FacultyAdmin(admin.ModelAdmin):
#     inlines = [StudentInline]

# @admin.register(Speciality)
# class SpecialityAdmin(admin.ModelAdmin):
#     inlines = [StudentInline]

# @admin.register(Discipline)
# class DisciplineAdmin(admin.ModelAdmin):
#     # inlines = [GradeInline]
#     list_display = ('name',)

# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     inlines = [StudentInline, GradeInline]

# admin.site.register(Language)
# admin.site.register(News)
# admin.site.register(Notification)
# admin.site.register(Application)
# admin.site.register(Instructor)
from django import forms
from django.contrib import admin
from .models import (Student, Faculty, StudentOfFaculty, Speciality, Teacher, Subject, Language, 
                     StudentStatus, News, Notification, Application, ApplicationStatus, 
                     StudentOfLanguage, StudentOfSpeciality, TypeOfGrades, Grade)

# class StudentOfFacultyInline(admin.TabularInline):
#     model = StudentOfFaculty
#     extra = 1
#     fields = ('student', 'faculty', 'start_date', 'end_date', 'is_current')
#     readonly_fields = ('is_current',)
#     verbose_name_plural = 'StudentOfFaculty'

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         return qs.order_by('-is_current')



class StudentOfFacultyForm(forms.ModelForm):
    class Meta:
        model = StudentOfFaculty
        fields = '__all__'

class StudentOfFacultyFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.fields['is_current'].widget = forms.Select(choices=[(True, 'Yes'), (False, 'No')])

class StudentOfFacultyInline(admin.TabularInline):
    model = StudentOfFaculty
    form = StudentOfFacultyForm
    extra = 1
    formset = StudentOfFacultyFormSet
    # readonly_fields = ('is_current',)
    verbose_name_plural = 'Faculties'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-is_current')
    
# ----------------------------------------------------------------------------------------

class StudentOfSpecialityForm(forms.ModelForm):
    class Meta:
        model = StudentOfSpeciality
        fields = '__all__'

class StudentOfSpecialityFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.fields['is_current'].widget = forms.Select(choices=[(True, 'Yes'), (False, 'No')])

class StudentOfSpecialityInline(admin.TabularInline):
    model = StudentOfSpeciality
    form = StudentOfSpecialityForm
    extra = 1
    formset = StudentOfSpecialityFormSet
    # readonly_fields = ('is_current',)
    verbose_name_plural = 'Specialies'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-is_current')


# -----------------------------------------------------------------------------------------------------

class StudentOfLanguageForm(forms.ModelForm):
    class Meta:
        model = StudentOfLanguage
        fields = '__all__'

class StudentOfLanguageFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.fields['is_current'].widget = forms.Select(choices=[(True, 'Yes'), (False, 'No')])

class StudentOfLanguageInline(admin.TabularInline):
    model = StudentOfLanguage
    form = StudentOfLanguageForm
    extra = 1
    formset = StudentOfLanguageFormSet
    # readonly_fields = ('is_current',)
    verbose_name_plural = 'Languagies'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-is_current')



@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('formatted_id', 'last_name', 'first_name', 'middle_name', 'date_of_birth', 'email', 'current_faculty', 'speciality', 'status')
    inlines = [StudentOfFacultyInline, StudentOfSpecialityInline, StudentOfLanguageInline]

    def formatted_id(self, obj):
        return f"{obj.id:06d}"

    formatted_id.short_description = 'ID'

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    inlines = [StudentOfFacultyInline]

@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    inlines = [StudentOfSpecialityInline]

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    inlines = [StudentOfLanguageInline]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('formatted_id', 'last_name', 'first_name', 'middle_name', 'date_of_birth', 'email')

    def formatted_id(self, obj):
        return f"{obj.id:06d}"

    formatted_id.short_description = 'ID'


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'teacher', 'grade_type', 'grade')
    
admin.site.register(TypeOfGrades)
admin.site.register(Subject)
admin.site.register(StudentStatus)
admin.site.register(News)
admin.site.register(Notification)
admin.site.register(Application)
admin.site.register(ApplicationStatus)
