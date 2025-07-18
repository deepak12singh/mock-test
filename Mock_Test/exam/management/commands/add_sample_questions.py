from django.core.management.base import BaseCommand
from exam.models import QuestionUG
import random

class Command(BaseCommand):
    help = 'Add sample Physics and Mathematics questions'

    def generate_math_questions(self):
        math_questions = [
            {
                'question': 'If $f(x) = x^2 + 2x + 1$, what is $f(3)$?',
                'option_a': '$12$',
                'option_b': '$14$',
                'option_c': '$16$',
                'option_d': '$18$',
                'correct_option': 'B'
            },
            {
                'question': 'Solve the equation: $2x + 5 = 13$',
                'option_a': '$x = 3$',
                'option_b': '$x = 4$',
                'option_c': '$x = 5$',
                'option_d': '$x = 6$',
                'correct_option': 'B'
            },
            # Template for more questions
            {
                'question': 'What is the derivative of $f(x) = x^3$?',
                'option_a': '$f\'(x) = x^2$',
                'option_b': '$f\'(x) = 2x$',
                'option_c': '$f\'(x) = 3x^2$',
                'option_d': '$f\'(x) = 3x$',
                'correct_option': 'C'
            },
        ]
        
        # Generate more math questions programmatically
        for i in range(97):  # We already have 3 questions above
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            operation = random.choice(['+', '-', '*'])
            
            if operation == '+':
                result = a + b
                question = f'Calculate: ${a} + {b}$'
            elif operation == '-':
                result = a - b
                question = f'Calculate: ${a} - {b}$'
            else:
                result = a * b
                question = f'Calculate: ${a} \\times {b}$'
            
            # Generate wrong options
            wrong_options = []
            while len(wrong_options) < 3:
                wrong = result + random.randint(-5, 5)
                if wrong != result and wrong not in wrong_options:
                    wrong_options.append(wrong)
            
            options = wrong_options + [result]
            random.shuffle(options)
            correct_index = options.index(result)
            correct_option = chr(65 + correct_index)  # Convert 0-3 to A-D
            
            math_questions.append({
                'question': question,
                'option_a': f'${options[0]}$',
                'option_b': f'${options[1]}$',
                'option_c': f'${options[2]}$',
                'option_d': f'${options[3]}$',
                'correct_option': correct_option
            })
        
        return math_questions

    def generate_physics_questions(self):
        physics_questions = [
            {
                'question': 'What is the SI unit of force?',
                'option_a': 'Newton (N)',
                'option_b': 'Joule (J)',
                'option_c': 'Watt (W)',
                'option_d': 'Pascal (Pa)',
                'correct_option': 'A'
            },
            {
                'question': 'The equation $F = ma$ is known as:',
                'option_a': "Newton's First Law",
                'option_b': "Newton's Second Law",
                'option_c': "Newton's Third Law",
                'option_d': 'Law of Conservation of Momentum',
                'correct_option': 'B'
            },
            {
                'question': 'What is the speed of light in vacuum?',
                'option_a': '$3 \\times 10^7$ m/s',
                'option_b': '$3 \\times 10^8$ m/s',
                'option_c': '$3 \\times 10^9$ m/s',
                'option_d': '$3 \\times 10^6$ m/s',
                'correct_option': 'B'
            },
        ]
        
        # Generate more physics questions programmatically
        formulas = [
            ('$v = u + at$', 'velocity', 'time', 'acceleration'),
            ('$s = ut + \\frac{1}{2}at^2$', 'displacement', 'time', 'acceleration'),
            ('$v^2 = u^2 + 2as$', 'velocity', 'displacement', 'acceleration'),
            ('$F = ma$', 'force', 'mass', 'acceleration'),
            ('$E = mc^2$', 'energy', 'mass', 'speed of light'),
            ('$P = \\frac{F}{A}$', 'pressure', 'force', 'area'),
            ('$W = Fs$', 'work', 'force', 'displacement'),
            ('$P = \\frac{W}{t}$', 'power', 'work', 'time'),
        ]
        
        for i in range(97):  # We already have 3 questions above
            if i < len(formulas) * 5:  # Use formulas for some questions
                formula, quantity1, quantity2, quantity3 = formulas[i % len(formulas)]
                question_types = [
                    f'Which formula correctly represents the relationship between {quantity1}, {quantity2}, and {quantity3}?',
                    f'In the formula {formula}, what does {random.choice([quantity1, quantity2, quantity3])} represent?',
                    f'If we increase {quantity1} in {formula}, what happens to {quantity2}?',
                ]
                question = random.choice(question_types)
            else:
                # Generate numerical physics problems
                mass = random.randint(1, 20)
                acceleration = random.randint(1, 10)
                force = mass * acceleration
                question = f'A body of mass ${mass}$ kg is subjected to an acceleration of ${acceleration}$ m/s². What is the force acting on it?'
                
                wrong_options = []
                while len(wrong_options) < 3:
                    wrong = force + random.randint(-5, 5)
                    if wrong > 0 and wrong != force and wrong not in wrong_options:
                        wrong_options.append(wrong)
                
                options = wrong_options + [force]
                random.shuffle(options)
                correct_index = options.index(force)
                correct_option = chr(65 + correct_index)
                
                physics_questions.append({
                    'question': question,
                    'option_a': f'${options[0]}$ N',
                    'option_b': f'${options[1]}$ N',
                    'option_c': f'${options[2]}$ N',
                    'option_d': f'${options[3]}$ N',
                    'correct_option': correct_option
                })
                continue
            
            # Generate options for formula-based questions
            options = [
                formula,
                formula.replace('+', '-'),
                formula.replace('2', '3'),
                formula.replace('\\frac{1}{2}', '\\frac{2}{3}')
            ]
            random.shuffle(options)
            correct_index = options.index(formula)
            correct_option = chr(65 + correct_index)
            
            physics_questions.append({
                'question': question,
                'option_a': options[0],
                'option_b': options[1],
                'option_c': options[2],
                'option_d': options[3],
                'correct_option': correct_option
            })
        
        return physics_questions

    def handle(self, *args, **kwargs):
        # Add Math questions
        math_questions = self.generate_math_questions()
        for q in math_questions:
            QuestionUG.objects.create(
                subject='Mathematics',
                question=q['question'],
                option_a=q['option_a'],
                option_b=q['option_b'],
                option_c=q['option_c'],
                option_d=q['option_d'],
                correct_option=q['correct_option']
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully added {len(math_questions)} Mathematics questions'))

        # Add Physics questions
        physics_questions = self.generate_physics_questions()
        for q in physics_questions:
            QuestionUG.objects.create(
                subject='Physics',
                question=q['question'],
                option_a=q['option_a'],
                option_b=q['option_b'],
                option_c=q['option_c'],
                option_d=q['option_d'],
                correct_option=q['correct_option']
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully added {len(physics_questions)} Physics questions'))

