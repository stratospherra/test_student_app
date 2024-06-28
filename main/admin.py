from django import forms
from django.contrib import admin
from .models import (Student, Faculty, StudentOfFaculty, Speciality, Teacher, Subject, Language, 
                     StudentStatus, News, Notification, Application, ApplicationStatus, 
                     StudentOfLanguage, StudentOfSpeciality, TypeOfGrades, Grade, 
                     DayOfWeek, ScheduleVersion, Schedule)



class StudentOfFacultyInline(admin.TabularInline):
    model = StudentOfFaculty
    extra = 1
    # formset = StudentOfFacultyFormSet
    verbose_name_plural = 'Faculties'
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-is_current')

class StudentOfSpecialityInline(admin.TabularInline):
    model = StudentOfSpeciality
    extra = 1
    # formset = StudentOfSpecialityFormSet
    verbose_name_plural = 'Specialies'
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-is_current')

class StudentOfLanguageInline(admin.TabularInline):
    model = StudentOfLanguage
    extra = 1
    # formset = StudentOfLanguageFormSet
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
admin.site.register(DayOfWeek)
admin.site.register(ScheduleVersion)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'time_start', 'time_end', 'subject', 'teacher', 'room')