# Generated by Django 4.1.7 on 2023-03-09 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("user_handler", "0001_initial"),
        ("tic_tac_toe", "0004_rename_gamecell_square"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="game",
            name="player_1",
        ),
        migrations.RemoveField(
            model_name="game",
            name="player_2",
        ),
        migrations.AddField(
            model_name="game",
            name="creator",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="creator",
                to="user_handler.user",
            ),
        ),
        migrations.AddField(
            model_name="game",
            name="opponent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="opponent",
                to="user_handler.user",
            ),
        ),
    ]
