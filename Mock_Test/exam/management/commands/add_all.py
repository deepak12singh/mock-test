from django.core.management.base import BaseCommand
from exam.models import QuestionPG  # replace 'yourapp' with actual app name
import random

MAIN_SUBJECTS = [
    "Hindi", "English", "Mathematics", "Reasoning", "Computer", "Micro Ecomonics", "Currency and banking",
    "Accounting", "Company law", "Business maths", "Indian writing", "Literary terms", "Literary genres",
    "Literary criticism", "Rachnakar", "Kaal vibhajan", "Jansanchar madhya", "Kavya shastra", "Vyakaran"
]

SUBJECT_MAPPING = {
    "Mathematics": "MCA",
    "Computer": "MCA",
    "Reasoning": "MCA",
    "Accounting": "M.Com",
    "Currency and banking": "M.Com",
    "Company law": "M.Com",
    "Business maths": "M.Com",
    "Micro Ecomonics": "M.Com",
    "Hindi": "MA (hindi)",
    "Vyakaran": "MA (hindi)",
    "Kaal vibhajan": "MA (hindi)",
    "Jansanchar madhya": "MA (hindi)",
    "Kavya shastra": "MA (hindi)",
    "Rachnakar": "MA (hindi)",
    "English": "M.A (English)",
    "Indian writing": "M.A (English)",
    "Literary terms": "M.A (English)",
    "Literary genres": "M.A (English)",
    "Literary criticism": "M.A (English)"
}

class Command(BaseCommand):
    help = 'Add sample PG questions for all main_subjects'

    def generate_question(self, main_subject):
        q_list = []
        for i in range(10):  # Add 10 sample questions per subject
            a = random.randint(1, 50)
            b = random.randint(1, 50)
            result = a + b
            options = [result, result+1, result-1, result+2]
            random.shuffle(options)
            correct_option = chr(65 + options.index(result))  # A-D
            q_list.append({
                'question': f'[{main_subject}] What is {a} + {b}?',
                'option_a': str(options[0]),
                'option_b': str(options[1]),
                'option_c': str(options[2]),
                'option_d': str(options[3]),
                'correct_option': correct_option,
            })
        return q_list

    def handle(self, *args, **kwargs):
        total = 0
        for subject in MAIN_SUBJECTS:
            pg_subject = SUBJECT_MAPPING.get(subject, "MBA")
            questions = self.generate_question(subject)
            for q in questions:
                QuestionPG.objects.create(
                    subject=pg_subject,
                    main_subject=subject,
                    question=q['question'],
                    option_a=q['option_a'],
                    option_b=q['option_b'],
                    option_c=q['option_c'],
                    option_d=q['option_d'],
                    correct_option=q['correct_option']
                )
            total += len(questions)
            self.stdout.write(self.style.SUCCESS(f'Added {len(questions)} questions for {subject} ({pg_subject})'))

        self.stdout.write(self.style.SUCCESS(f'Total questions added: {total}'))
