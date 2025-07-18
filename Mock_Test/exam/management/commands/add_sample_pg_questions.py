from django.core.management.base import BaseCommand
from exam.models import QuestionPG  # Replace 'yourapp' with your app name
import random

class Command(BaseCommand):
    help = 'Add sample Computer and Accounting questions to QuestionPG'

    def generate_computer_questions(self):
        questions = [
            {
                'question': 'What does CPU stand for?',
                'option_a': 'Central Performance Unit',
                'option_b': 'Central Processing Unit',
                'option_c': 'Control Processing Unit',
                'option_d': 'Central Program Unit',
                'correct_option': 'B'
            },
            {
                'question': 'HTML stands for?',
                'option_a': 'Hyper Trainer Marking Language',
                'option_b': 'Hyper Text Markup Language',
                'option_c': 'High Text Marking Language',
                'option_d': 'Hyper Tool Markup Language',
                'correct_option': 'B'
            },
        ]

        for i in range(98):  # Total 100 questions
            a = random.randint(1, 100)
            b = random.randint(1, 100)
            operation = random.choice(['+', '*', '-'])
            
            if operation == '+':
                result = a + b
                question_text = f'In programming, what is the output of print({a} + {b})?'
            elif operation == '-':
                result = a - b
                question_text = f'In programming, what is the output of print({a} - {b})?'
            else:
                result = a * b
                question_text = f'In programming, what is the output of print({a} * {b})?'

            wrong_options = set()
            while len(wrong_options) < 3:
                wrong = result + random.randint(-10, 10)
                if wrong != result:
                    wrong_options.add(wrong)

            options = list(wrong_options) + [result]
            random.shuffle(options)
            correct_option = chr(65 + options.index(result))  # A-D

            questions.append({
                'question': question_text,
                'option_a': f'{options[0]}',
                'option_b': f'{options[1]}',
                'option_c': f'{options[2]}',
                'option_d': f'{options[3]}',
                'correct_option': correct_option
            })

        return questions

    def generate_accounting_questions(self):
        concepts = [
            ("Double Entry System", "Every transaction has a dual effect"),
            ("Ledger", "A book where transactions are recorded"),
            ("Trial Balance", "A statement to check the arithmetical accuracy"),
            ("Journal", "The first book of entry"),
            ("Debit", "Left side of an account"),
            ("Credit", "Right side of an account"),
        ]

        questions = [
            {
                'question': 'Which statement is used to verify arithmetical accuracy of books?',
                'option_a': 'Balance Sheet',
                'option_b': 'Trial Balance',
                'option_c': 'Ledger',
                'option_d': 'Journal',
                'correct_option': 'B'
            },
            {
                'question': 'What is the left side of an account called?',
                'option_a': 'Credit',
                'option_b': 'Equity',
                'option_c': 'Debit',
                'option_d': 'Asset',
                'correct_option': 'C'
            },
        ]

        for i in range(98):  # Total 100 questions
            term, definition = random.choice(concepts)
            question = f'What best defines "{term}"?'

            wrong_defs = [d for t, d in concepts if d != definition]
            options = random.sample(wrong_defs, 3) + [definition]
            random.shuffle(options)
            correct_option = chr(65 + options.index(definition))

            questions.append({
                'question': question,
                'option_a': options[0],
                'option_b': options[1],
                'option_c': options[2],
                'option_d': options[3],
                'correct_option': correct_option
            })

        return questions

    def handle(self, *args, **kwargs):
        computer_questions = self.generate_computer_questions()
        for q in computer_questions:
            QuestionPG.objects.create(
                subject='MCA',
                main_subject='Computer',
                question=q['question'],
                option_a=q['option_a'],
                option_b=q['option_b'],
                option_c=q['option_c'],
                option_d=q['option_d'],
                correct_option=q['correct_option']
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully added {len(computer_questions)} Computer questions'))

        accounting_questions = self.generate_accounting_questions()
        for q in accounting_questions:
            QuestionPG.objects.create(
                subject='M.Com',
                main_subject='Accounting',
                question=q['question'],
                option_a=q['option_a'],
                option_b=q['option_b'],
                option_c=q['option_c'],
                option_d=q['option_d'],
                correct_option=q['correct_option']
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully added {len(accounting_questions)} Accounting questions'))
