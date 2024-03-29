# Generated by Django 5.0.2 on 2024-02-21 22:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('booked_at', models.DateTimeField()),
                ('date', models.DateField()),
                ('booked', models.CharField(default='Available', max_length=100)),
                ('booked_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('booked_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booked_for', to=settings.AUTH_USER_MODEL)),
                ('time_slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.timeslot')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
