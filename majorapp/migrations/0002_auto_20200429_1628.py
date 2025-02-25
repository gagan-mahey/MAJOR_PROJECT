# Generated by Django 3.0.4 on 2020-04-29 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('majorapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(max_length=250)),
                ('cover_pic', models.FileField(upload_to='media/%Y/%m/%d')),
                ('description', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='contact_us',
            name='contact_number',
            field=models.IntegerField(),
        ),
    ]
