# Generated by Django 4.2.4 on 2023-09-20 17:13

import dishes.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Basket",
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
                ("quantity", models.PositiveSmallIntegerField(default=0)),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="DishType",
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
                ("name", models.CharField(max_length=63, unique=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Dish",
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
                ("name", models.CharField(max_length=250, unique=True)),
                ("description", models.TextField()),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=7,
                        validators=[
                            django.core.validators.MinValueValidator(limit_value=0)
                        ],
                    ),
                ),
                (
                    "image",
                    models.ImageField(upload_to=dishes.models.dish_image_file_path),
                ),
                (
                    "dish_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dishes",
                        to="dishes.dishtype",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "dishes",
                "ordering": ["name"],
            },
        ),
    ]
