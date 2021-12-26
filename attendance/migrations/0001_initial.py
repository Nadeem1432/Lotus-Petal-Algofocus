# Generated by Django 3.2.3 on 2021-12-15 02:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('timetable', '0001_initial'),
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreOnlineAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=50, unique=True)),
                ('topic_name', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('attendance_status', models.JSONField(blank=True, null=True)),
                ('wrong_emails', models.JSONField(blank=True, null=True)),
                ('is_marked', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('period', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='timetable.timetable')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.section')),
            ],
        ),
        migrations.CreateModel(
            name='StoreOfflineAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('attendance_status', models.JSONField()),
                ('is_stored', models.BooleanField(default=True)),
                ('is_marked', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.timetable')),
            ],
        ),
    ]