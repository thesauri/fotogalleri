# Generated by Django 2.2.5 on 2019-10-17 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureGate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('feature_groups', models.ManyToManyField(related_name='featuregate', to='auth.Group')),
            ],
        ),
    ]
