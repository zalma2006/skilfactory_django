# Generated by Django 4.1.2 on 2023-01-22 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("D5", "0003_alter_category_subscribers"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name_category",
            field=models.CharField(
                help_text="category name", max_length=255, unique=True
            ),
        ),
        migrations.CreateModel(
            name="MyModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "kind",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="kinds",
                        to="D5.category",
                        verbose_name="This is the help text",
                    ),
                ),
            ],
        ),
    ]