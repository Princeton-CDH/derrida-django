# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-10 20:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0028_add_DerridaWorkBook'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='derridaworkbook',
            options={'verbose_name': 'Edition - Derrida work relation', 'verbose_name_plural': 'Edition - Derrida work relations'},
        ),
        migrations.AlterField(
            model_name='book',
            name='original_pub_info',
            field=models.TextField(blank=True, null=True, verbose_name='Original Publication Information'),
        ),
        migrations.AlterField(
            model_name='derridaworkbook',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_edition', to='books.Book', verbose_name='Cited edition'),
        ),
        migrations.AlterField(
            model_name='derridaworkbook',
            name='derridawork',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='self_work', to='books.DerridaWork', verbose_name='Cited in'),
        ),
    ]
