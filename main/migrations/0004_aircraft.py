# Generated by Django 4.2.17 on 2025-01-03 07:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0003_alter_avionics_options_alter_fuselage_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Aircraft",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "aircraft_type",
                    models.CharField(
                        choices=[
                            ("TB2", "Tb2"),
                            ("TB3", "Tb3"),
                            ("AKINCI", "Akinci"),
                            ("KIZILELMA", "Kizilelma"),
                        ],
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "avionics_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.avionics"
                    ),
                ),
                (
                    "fuselage_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.fuselage"
                    ),
                ),
                (
                    "tail_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.tail"
                    ),
                ),
                (
                    "wing_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.wing"
                    ),
                ),
            ],
            options={
                "permissions": [
                    ("create_aircraft", "Can create aircraft"),
                    ("view_create_aircraft_page", "Can view create aircraft page"),
                ],
            },
        ),
    ]
