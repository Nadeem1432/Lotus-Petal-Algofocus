# Generated by Django 3.2.3 on 2021-12-20 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('substitution', '0002_auto_20211215_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='substitution',
            name='substituted',
            field=models.BooleanField(default=True),
        ),
    ]
