# Generated by Django 4.2.4 on 2023-09-24 20:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("dishes", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="dish",
            name="likes",
            field=models.ManyToManyField(
                blank=True, related_name="dishes", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="basket",
            name="dish",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="baskets",
                to="dishes.dish",
            ),
        ),
        migrations.AddField(
            model_name="basket",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="baskets",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
