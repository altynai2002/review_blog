# Generated by Django 3.1 on 2021-01-25 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='budget',
            field=models.PositiveIntegerField(default=0, help_text='на одного человека в сомах'),
        ),
    ]
