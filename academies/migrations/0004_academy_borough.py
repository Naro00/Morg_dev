# Generated by Django 4.1 on 2022-09-07 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("academies", "0003_alter_academy_options_alter_event_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="academy",
            name="borough",
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
