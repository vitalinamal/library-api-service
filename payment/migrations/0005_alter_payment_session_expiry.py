# Generated by Django 5.0.6 on 2024-06-17 08:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0004_alter_payment_session_expiry"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="session_expiry",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 6, 18, 8, 47, 5, 603501, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
