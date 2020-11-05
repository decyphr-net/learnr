# Generated by Django 3.1.1 on 2020-11-05 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=8)),
                ('short_code', models.CharField(max_length=2)),
                ('description', models.TextField()),
            ],
        ),
    ]
