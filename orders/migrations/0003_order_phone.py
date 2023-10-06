# Generated by Django 4.2.4 on 2023-10-04 18:39

import phonenumber_field.modelfields
from django.db import migrations

import users.models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0002_alter_order_basket_history_alter_order_initiator"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="phone",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True,
                default="",
                max_length=128,
                region="UA",
                validators=[users.models.validate_ukrainian_phone_number],
            ),
        ),
    ]
