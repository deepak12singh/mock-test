# Generated by Django 5.1.4 on 2025-04-17 03:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0006_testattempt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='testattempt',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='testattempt',
            name='user',
        ),
        migrations.DeleteModel(
            name='NotTouchedOption',
        ),
        migrations.DeleteModel(
            name='Result',
        ),
        migrations.DeleteModel(
            name='TestAttempt',
        ),
    ]
