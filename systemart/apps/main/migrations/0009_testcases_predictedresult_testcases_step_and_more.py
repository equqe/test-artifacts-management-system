# Generated by Django 5.0.2 on 2024-05-31 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_rename_creationdate_bugreports_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='testcases',
            name='predictedresult',
            field=models.TextField(default=1, max_length=512),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testcases',
            name='step',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='CaseSteps',
        ),
    ]
