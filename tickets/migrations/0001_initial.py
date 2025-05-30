# Generated by Django 4.2.20 on 2025-05-05 20:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def seed_status_and_priority(apps, schema_editor):
    Status = apps.get_model('tickets', 'Status')
    Priority = apps.get_model('tickets', 'Priority')

    Status.objects.bulk_create([
        Status(name='Nouveau', order=1, color='#3498db'),
        Status(name='En cours', order=2, color='#f1c40f'),
        Status(name='Résolu', order=3, color='#2ecc71'),
        Status(name='Fermé', order=4, color='#95a5a6'),
    ])

    Priority.objects.bulk_create([
        Priority(name='Basse', level=1),
        Priority(name='Moyenne', level=2),
        Priority(name='Haute', level=3),
        Priority(name='Critique', level=4),
    ])


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('level', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('order', models.PositiveIntegerField(default=0)),
                ('color', models.CharField(blank=True, max_length=7, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                  related_name='assigned_tickets', to=settings.AUTH_USER_MODEL)),
                ('category',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tickets.category')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets',
                                                 to=settings.AUTH_USER_MODEL)),
                ('priority',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tickets.priority')),
                ('status',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tickets.status')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
            },

        ),
        migrations.RunPython(seed_status_and_priority),
    ]
