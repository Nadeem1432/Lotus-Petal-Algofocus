# Generated by Django 3.2.3 on 2021-12-15 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('substitution', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='substitution',
            name='substitution_month',
        ),
        migrations.RemoveField(
            model_name='substitution',
            name='substitution_week',
        ),
        migrations.RemoveField(
            model_name='substitution',
            name='substitution_year',
        ),
    ]
