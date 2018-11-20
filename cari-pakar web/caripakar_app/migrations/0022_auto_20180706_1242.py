# Generated by Django 2.0.6 on 2018-07-06 12:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caripakar_app', '0021_auto_20180706_0742'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalVar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterModelOptions(
            name='jabatanfungsional',
            options={'ordering': ('rank',)},
        ),
        migrations.AlterModelOptions(
            name='jenjang',
            options={'ordering': ('rank',)},
        ),
        migrations.AlterField(
            model_name='jabatanfungsional',
            name='skor_jabatanfungsional',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='jenjang',
            name='skor_jenjang',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]),
        ),
    ]
