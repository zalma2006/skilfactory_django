# Generated by Django 4.1.5 on 2023-02-26 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mmorgnews", "0005_alter_author_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="author",
            name="user",
        ),
        migrations.AddField(
            model_name="author",
            name="author",
            field=models.CharField(default=False, max_length=150, unique=True),
        ),
    ]
