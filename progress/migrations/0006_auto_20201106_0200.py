# Generated by Django 3.1.1 on 2020-11-06 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0005_auto_20201022_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progress',
            name='passed',
            field=models.CharField(blank=True, choices=[('Y', 'Yes'), ('N', 'No'), ('NA', 'NOT APPLICABLE')], default='NA', max_length=20, null=True),
        ),
    ]
