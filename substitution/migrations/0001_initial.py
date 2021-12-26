# Generated by Django 3.2.3 on 2021-12-15 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('timetable', '0003_delete_substitution'),
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Substitution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_online', models.BooleanField(default=False)),
                ('substitution_date', models.DateField(blank=True, null=True)),
                ('substitution_month', models.IntegerField(blank=True, null=True)),
                ('substitution_year', models.IntegerField(blank=True, null=True)),
                ('substitution_week', models.IntegerField(blank=True, null=True)),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.day')),
                ('period_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.period')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.section')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.teacher')),
            ],
            options={
                'unique_together': {('day', 'period_no', 'section')},
            },
        ),
    ]