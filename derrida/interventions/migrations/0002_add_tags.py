# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-20 16:10
from __future__ import unicode_literals

from django.core.management import call_command
from django.db import migrations, models

def load_initial_tags(apps, schema_editor):
    call_command('loaddata', 'initial_tags', app_label='interventions',
                 verbose=0)


class Migration(migrations.Migration):

    dependencies = [
        ('interventions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('notes', models.TextField(blank=True)),
                ('applies_to', models.CharField(choices=[('A', 'Annotations only'), ('I', 'Insertions only'), ('AI', 'Both Annotations and Insertions')], default='AI', help_text='Type or types of interventions this tag is applicable to.', max_length=2)),
            ],
            options={
                'abstract': False,
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='intervention',
            name='tags',
            field=models.ManyToManyField(blank=True, to='interventions.Tag'),
        ),
        # load an initial set of intervention tags
        migrations.RunPython(
            code=load_initial_tags,
            reverse_code=migrations.RunPython.noop,
        ),

    ]