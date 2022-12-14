# Generated by Django 4.1.2 on 2022-12-29 18:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("D5", "0002_category_subscribers"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="subscribers",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="categories",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
