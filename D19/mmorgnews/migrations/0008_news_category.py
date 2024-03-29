# Generated by Django 4.1.5 on 2023-03-02 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mmorgnews", "0007_alter_author_author"),
    ]

    operations = [
        migrations.AddField(
            model_name="news",
            name="category",
            field=models.ManyToManyField(
                through="mmorgnews.NewsCategory", to="mmorgnews.category"
            ),
        ),
    ]
