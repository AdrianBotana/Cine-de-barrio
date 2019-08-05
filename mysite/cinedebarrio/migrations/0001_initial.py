# Generated by Django 2.0.5 on 2018-05-27 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=200)),
                ('year', models.IntegerField()),
                ('director', models.CharField(max_length=50)),
                ('actors', models.CharField(max_length=200)),
                ('poster', models.CharField(max_length=300)),
                ('score', models.FloatField()),
            ],
        ),
    ]