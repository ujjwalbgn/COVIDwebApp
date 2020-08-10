# Generated by Django 3.0.7 on 2020-08-09 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0006_contacttracing_periodicreporting'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='diagnosis',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='have_you_been_tested_positive_for_COVID',
            field=models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='lab_reports',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='pre_existing_conditions',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='periodicreporting',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
