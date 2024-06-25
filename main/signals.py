from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import TypeOfGrades

@receiver(post_migrate)
def create_grade_types(sender, **kwargs):
    if sender.name == 'main':  
        grades = [
            ('ср.т1', True),
            ('ср.т2', True),
            ('рк1', True),
            ('Р1', True),
            ('рк2', True),
            ('Р2', True),
            ('Общий Рейтинг', True),
            ('Экзамен', True),
            ('итог оценка', True),
        ]

        for title, calculate in grades:
            TypeOfGrades.objects.get_or_create(title=title, calculate=calculate)
