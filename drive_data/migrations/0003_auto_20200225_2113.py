# Generated by Django 3.0.3 on 2020-02-25 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drive_data', '0002_file_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='File_Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(default=None, upload_to='uploads/')),
                ('name', models.CharField(max_length=257)),
            ],
        ),
        migrations.AlterField(
            model_name='file',
            name='date_created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='folder',
            name='date_created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]