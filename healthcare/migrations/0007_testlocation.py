# Generated by Django 3.0.8 on 2020-08-03 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0006_auto_20200802_2037'),
    ]

    operations = [
        migrations.CreateModel(
            name='testLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=500, null=True)),
                ('phone_number', models.CharField(max_length=200, null=True)),
                ('website', models.CharField(max_length=500, null=True)),
                ('email', models.CharField(max_length=500, null=True)),
            ],
        ),
    ]
