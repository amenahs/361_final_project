

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseID', models.CharField(max_length=40)),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('email', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=20)),
                ('phoneNumber', models.IntegerField()),
                ('homeAddress', models.CharField(max_length=75)),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='final_project.professor')),
                ('taID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='final_project.ta')),
            ],
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('labID', models.CharField(max_length=3)),
                ('taID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='final_project.ta')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coursesTaught', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='final_project.course')),
            ],
        ),
    ]
