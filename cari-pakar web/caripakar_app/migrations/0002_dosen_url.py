# Generated by Django 2.0.5 on 2018-06-27 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caripakar_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dosen',
            name='url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
