import os
import pandas as pd
from django.core.management.base import BaseCommand
from exam.models import QuestionUG  # Adjust app name if needed

class Command(BaseCommand):
    help = 'Import all .xlsx or .csv files from a folder into QuestionUG model'

    def handle(self, *args, **kwargs):
        folder_path = 'media/uploads/questions/UG'
        files = [f for f in os.listdir(folder_path) if f.endswith(('.xlsx', '.csv'))]

        if not files:
            self.stdout.write(self.style.WARNING('No .xlsx or .csv files found in the folder.'))
            return

        total_imported = 0
        for file in files:
            file_path = os.path.join(folder_path, file)
            self.stdout.write(self.style.NOTICE(f'Processing file: {file_path}'))

            try:
                if file.endswith('.xlsx'):
                    df = pd.read_excel(file_path)
                else:
                    df = pd.read_csv(file_path)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to read {file}: {e}"))
                continue

            # Rename actual columns to match model field names
            df = df.rename(columns={
                'Questions': 'question',
                'A': 'option_a',
                'B': 'option_b',
                'C': 'option_c',
                'D': 'option_d',
                'correct option': 'correct_option',
                'subject': 'subject'
            })

            required_columns = [
                'question', 'option_a', 'option_b', 'option_c',
                'option_d', 'correct_option', 'subject'
            ]
            if not all(col in df.columns for col in required_columns):
                self.stdout.write(self.style.ERROR(f"Missing required columns after renaming in file {file}"))
                continue

            imported = 0
            for _, row in df.iterrows():
                try:
                    QuestionUG.objects.create(
                        question=row['question'],
                        option_a=row['option_a'],
                        option_b=row['option_b'],
                        option_c=row['option_c'],
                        option_d=row['option_d'],
                        correct_option=str(row['correct_option']).strip().upper()[0],
                        subject=str(row['subject']).strip().capitalize()
                    )
                    imported += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Skipped a row due to error: {e}"))

            total_imported += imported
            self.stdout.write(self.style.SUCCESS(f"Imported {imported} rows from {file}"))

        self.stdout.write(self.style.SUCCESS(f"Total questions imported: {total_imported}"))
