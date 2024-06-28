from django.shortcuts import render
from main.models import DayOfWeek, Language


def index(request):
    return render(request, 'index.html')


# def add_days_of_week():
#     english, _ = Language.objects.get_or_create(name='English')
#     russian, _ = Language.objects.get_or_create(name='Русский')
#     kazakh, _ = Language.objects.get_or_create(name='Қазақша')

#     days_en = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#     days_ru = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
#     days_kz = ['Дүйсенбі', 'Сейсенбі', 'Сәрсенбі', 'Бейсенбі', 'Жұма', 'Сенбі', 'Жексенбі']

#     for day in days_en:
#         DayOfWeek.objects.get_or_create(name=day, language=english)

#     for day in days_ru:
#         DayOfWeek.objects.get_or_create(name=day, language=russian)

#     for day in days_kz:
#         DayOfWeek.objects.get_or_create(name=day, language=kazakh)