# Generated by Django 4.2.4 on 2023-10-04 15:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                ("first_name", models.CharField(max_length=64)),
                ("last_name", models.CharField(max_length=64)),
                ("email", models.EmailField(max_length=254)),
                ("address", models.CharField(max_length=256)),
                ("basket_history", models.JSONField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.SmallIntegerField(
                        choices=[
                            (0, "created"),
                            (1, "paid"),
                            (2, "on_way"),
                            (3, "delivered"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "initiator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]