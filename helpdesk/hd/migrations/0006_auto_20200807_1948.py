# Generated by Django 3.0.9 on 2020-08-07 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hd', '0005_auto_20200807_1938'),
    ]

    operations = [
        migrations.RenameField(
            model_name='claimmodel',
            old_name='user_id',
            new_name='author',
        ),
    ]
