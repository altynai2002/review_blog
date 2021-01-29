# Generated by Django 3.1 on 2021-01-29 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True),
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]