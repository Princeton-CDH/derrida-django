# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-13 23:16
from __future__ import unicode_literals
import os
from django.conf import settings
from django.core.management import call_command
import django.core.validators
from django.db import migrations, models
import django.db.migrations.operations.special
import django.db.models.deletion
import sortedm2m.fields
from derrida.utils import LoadFixtureData, reset_sqlsequence

# Custom migration functions manually adapted rom squashed migrations

# derrida.books.migrations.0006_initial_languages
def load_initial_languages(apps, schema_editor):
    Language = apps.get_model('books', 'Language')
    for lang in ['French', 'German', 'English']:
        Language.objects.get_or_create(name=lang)

# derrida.books.migrations.0010_initial_reftypes
def load_initial_reftypes(apps, schema_editor):
    call_command('loaddata', 'initial_reftypes', app_label='books', verbose=0)

# derrida.books.migrations.0020_add_initial_item_types
# - no longer needed, item types has been removed

# derrida.books.migrations.0031_migrate_books_to_works_instances
# - no longer needed, no book data to migrate after squashing


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('people', '0002_allow_neg_years_bc'),
        ('places', '0001_initial'),
    ]

    operations = [
        # NOTE: model creation and fields here were regenerated
        # based on a fresh initial migration for the models in their current
        # rather than try to reconcile the history of creating, modifying,
        # and removing the obsolete book models and things that referenced them.

        migrations.CreateModel(
            name='CreatorType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('notes', models.TextField(blank=True)),
                ('uri', models.URLField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='DerridaWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True)),
                ('short_title', models.CharField(max_length=255)),
                ('full_citation', models.TextField()),
                ('is_primary', models.BooleanField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True)),
                ('alternate_title', models.CharField(blank=True, max_length=255)),
                ('zotero_id', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('\\W', inverse_match=True, message='Zotero IDs must be alphanumeric.')])),
                ('is_extant', models.BooleanField(default=False, help_text='Extant in PUL JD')),
                ('is_annotated', models.BooleanField(default=False)),
                ('is_translation', models.BooleanField(default=False)),
                ('dimensions', models.CharField(blank=True, max_length=255)),
                ('copyright_year', models.PositiveIntegerField(blank=True, null=True)),
                ('print_date', models.DateField(blank=True, help_text='Date as YYYY-MM-DD, YYYY-MM, or YYYY format. Use print date day/month/year known flags to indicate that the information is not known.', null=True, verbose_name='Print Date')),
                ('print_date_day_known', models.BooleanField(default=False)),
                ('print_date_month_known', models.BooleanField(default=False)),
                ('print_date_year_known', models.BooleanField(default=True)),
                ('uri', models.URLField(blank=True, default='', help_text='Finding Aid URL for items in PUL Derrida Library', verbose_name='URI')),
                ('has_dedication', models.BooleanField(default=False)),
                ('has_insertions', models.BooleanField(default=False)),
                ('start_page', models.CharField(blank=True, max_length=20, null=True)),
                ('end_page', models.CharField(blank=True, max_length=20, null=True)),
                ('cited_in', models.ManyToManyField(blank=True, help_text='Derrida works that cite this edition or instance', to='books.DerridaWork')),
                ('collected_in', models.ForeignKey(blank=True, help_text='Larger work instance that collects or includes this item', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='collected_set', to='books.Instance')),
            ],
            options={
                'verbose_name': 'Derrida library work instance',
                'ordering': ['alternate_title', 'work__primary_title'],
            },
        ),
        migrations.CreateModel(
            name='InstanceCatalogue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True)),
                ('start_year', models.SmallIntegerField(blank=True, null=True)),
                ('end_year', models.SmallIntegerField(blank=True, null=True)),
                ('is_current', models.BooleanField()),
                ('call_number', models.CharField(blank=True, help_text='Used for Derrida shelf mark', max_length=255, null=True)),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Instance')),
            ],
            options={
                'verbose_name': 'Catalogue',
            },
        ),
        migrations.CreateModel(
            name='InstanceCreator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True)),
                ('creator_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.CreatorType')),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Instance')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.Person')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InstanceLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True)),
                ('is_primary', models.BooleanField()),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Instance')),
            ],
            options={
                'verbose_name': 'Language',
            },
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('notes', models.TextField(blank=True)),
                ('uri', models.URLField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='OwningInstitution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('notes', models.TextField(blank=True)),
                ('short_name', models.CharField(blank=True, help_text='Optional short name for admin display', max_length=255)),
                ('contact_info', models.TextField()),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.Place')),
            ],
            options={
                'abstract': False,
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PersonBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True)),
                ('start_year', models.SmallIntegerField(blank=True, null=True)),
                ('end_year', models.SmallIntegerField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Instance')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.Person')),
            ],
            options={
                'verbose_name': 'Person/Book Interaction',
            },
        ),
        migrations.CreateModel(
            name='PersonBookRelationshipType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('notes', models.TextField(blank=True)),
                ('uri', models.URLField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('derridawork_page', models.CharField(max_length=10)),
                ('derridawork_pageloc', models.CharField(max_length=2)),
                ('book_page', models.CharField(blank=True, max_length=255)),
                ('anchor_text', models.TextField(blank=True)),
                ('derridawork', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.DerridaWork')),
                ('instance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='books.Instance')),
            ],
            options={
                'ordering': ['derridawork', 'derridawork_page', 'derridawork_pageloc'],
            },
        ),
        migrations.CreateModel(
            name='ReferenceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('notes', models.TextField(blank=True)),
                ('uri', models.URLField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True)),
                ('primary_title', models.TextField()),
                ('short_title', models.CharField(max_length=255)),
                ('year', models.IntegerField(blank=True, help_text='Original publication date', null=True)),
                ('uri', models.URLField(blank=True, default='', help_text='Linked data URI', verbose_name='URI')),
                ('authors', models.ManyToManyField(to='people.Person')),
            ],
            options={
                'verbose_name': 'Derrida library work',
                'ordering': ['primary_title'],
            },
        ),
        migrations.CreateModel(
            name='WorkLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True)),
                ('is_primary', models.BooleanField()),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Language')),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Work')),
            ],
            options={
                'verbose_name': 'Language',
            },
        ),
        migrations.CreateModel(
            name='WorkSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True)),
                ('is_primary', models.BooleanField(default=False)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Subject')),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Work')),
            ],
            options={
                'verbose_name': 'Subject',
            },
        ),
        migrations.AddField(
            model_name='work',
            name='languages',
            field=models.ManyToManyField(through='books.WorkLanguage', to='books.Language'),
        ),
        migrations.AddField(
            model_name='work',
            name='subjects',
            field=models.ManyToManyField(through='books.WorkSubject', to='books.Subject'),
        ),
        migrations.AddField(
            model_name='reference',
            name='reference_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.ReferenceType'),
        ),
        migrations.AddField(
            model_name='personbook',
            name='relationship_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.PersonBookRelationshipType'),
        ),
        migrations.AddField(
            model_name='instancelanguage',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Language'),
        ),
        migrations.AddField(
            model_name='instancecatalogue',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.OwningInstitution'),
        ),
        migrations.AddField(
            model_name='instance',
            name='journal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='books.Journal'),
        ),
        migrations.AddField(
            model_name='instance',
            name='languages',
            field=models.ManyToManyField(through='books.InstanceLanguage', to='books.Language'),
        ),
        migrations.AddField(
            model_name='instance',
            name='owning_institutions',
            field=models.ManyToManyField(through='books.InstanceCatalogue', to='books.OwningInstitution'),
        ),
        migrations.AddField(
            model_name='instance',
            name='pub_place',
            field=sortedm2m.fields.SortedManyToManyField(blank=True, help_text=None, to='places.Place', verbose_name='Place(s) of Publication'),
        ),
        migrations.AddField(
            model_name='instance',
            name='publisher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='books.Publisher'),
        ),
        migrations.AddField(
            model_name='instance',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.Work'),
        ),
        migrations.AlterUniqueTogether(
            name='worksubject',
            unique_together=set([('subject', 'work')]),
        ),
        migrations.AlterUniqueTogether(
            name='worklanguage',
            unique_together=set([('work', 'language')]),
        ),
        migrations.AlterUniqueTogether(
            name='instancelanguage',
            unique_together=set([('instance', 'language')]),
        ),

        migrations.RunPython(
            code=load_initial_languages,
            reverse_code=migrations.RunPython.noop,
        ),

        migrations.RunPython(
            code=load_initial_reftypes,
            reverse_code=migrations.RunPython.noop,
        ),

        migrations.RunPython(
            code=LoadFixtureData(*[os.path.join(
                    settings.BASE_DIR, 'derrida', 'books', 'fixtures',
                    'initial_derridawork.json'
                )]
            ),
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.RunPython(
            code=reset_sqlsequence,
            reverse_code=migrations.RunPython.noop,
        ),

        # data migration not needed in squashed migration
        # migrations.RunPython(
            # code=derrida.books.migrations.0031_migrate_books_to_works_instances.books_to_works_instances,
            # reverse_code=derrida.books.migrations.0031_migrate_books_to_works_instances.remove_works_instances,
        # ),
    ]
