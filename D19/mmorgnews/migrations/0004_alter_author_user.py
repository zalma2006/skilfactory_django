# Generated by Django 4.1.5 on 2023-02-26 15:12

import annoying.fields
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mmorgnews", "0003_alter_author_user_alter_users_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="author",
            name="user",
            field=annoying.fields.AutoOneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="mmorgnews.users"
            ),
        ),
    ]
