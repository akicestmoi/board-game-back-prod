# Generated by Django 4.1.7 on 2023-03-17 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_handler", "0003_remove_user_createdat"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(max_length=500),
        ),
    ]
