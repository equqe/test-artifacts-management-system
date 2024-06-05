# Generated by Django 5.0.2 on 2024-06-05 13:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testcases',
            name='predictedresult',
        ),
        migrations.RemoveField(
            model_name='testcases',
            name='step',
        ),
        migrations.CreateModel(
            name='CaseSteps',
            fields=[
                ('step_id', models.AutoField(primary_key=True, serialize=False)),
                ('step', models.TextField(blank=True, max_length=512, null=True)),
                ('predictedresult', models.TextField(blank=True, max_length=512, null=True)),
                ('testcase_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='main.testcases')),
            ],
        ),
    ]
