# Generated by Django 4.1.1 on 2022-09-08 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="email_confirmed",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="user",
            name="Currency",
            field=models.CharField(
                blank=True, choices=[("krw", "KRW")], default="krw", max_length=3
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="language",
            field=models.CharField(
                blank=True,
                choices=[("en", "English"), ("ko", "Korean")],
                default="ko",
                max_length=2,
            ),
        ),
    ]
