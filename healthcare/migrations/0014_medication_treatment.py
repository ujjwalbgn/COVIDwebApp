# Generated by Django 3.0.7 on 2020-08-04 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0013_auto_20200803_2058'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('description', models.CharField(blank=True, max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('description', models.CharField(blank=True, max_length=2000)),
            ],
        ),
    ]
