# Generated by Django 3.0.9 on 2020-08-07 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hd', '0004_auto_20200807_1501'),
    ]

    operations = [
        migrations.RenameField(
            model_name='claimmodel',
            old_name='author',
            new_name='user_id',
        ),
    ]
