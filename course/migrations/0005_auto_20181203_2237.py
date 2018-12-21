# Generated by Django 2.1.2 on 2018-12-03 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_auto_20181023_1918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='alias',
        ),
        migrations.AddField(
            model_name='course',
            name='language',
            field=models.CharField(choices=[(0, 'Python'), (1, 'C'), (2, 'C++'), (3, 'Java')], default=0, max_length=15),
            preserve_default=False,
        ),
    ]
