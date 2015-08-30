# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('user', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'accounts',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('message', models.TextField(max_length=4000)),
                ('updated', models.DateField()),
                ('fk_account', models.ForeignKey(db_column='fk_account', to='welcome.Account')),
            ],
            options={
                'db_table': 'message',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=250)),
                ('updated', models.DateField()),
            ],
            options={
                'db_table': 'tickets',
            },
        ),
        migrations.AddField(
            model_name='message',
            name='fk_ticket',
            field=models.ForeignKey(db_column='fk_ticket', to='welcome.Ticket'),
        ),
    ]
