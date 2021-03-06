# Generated by Django 2.2.7 on 2019-12-08 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_auto_20191017_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagepath',
            name='path',
            field=models.CharField(max_length=256),
        ),
        migrations.AddConstraint(
            model_name='imagepath',
            constraint=models.UniqueConstraint(fields=('parent', 'path'), name='unique_path'),
        ),
    ]
