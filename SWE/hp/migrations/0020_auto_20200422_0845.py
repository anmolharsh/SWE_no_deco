# Generated by Django 3.0.4 on 2020-04-22 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hp', '0019_visitor_visitor_names'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visitor',
            old_name='visitor_names',
            new_name='visitor_details',
        ),
    ]