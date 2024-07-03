# Generated by Django 4.2.13 on 2024-07-03 12:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("images", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="total_likes",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddIndex(
            model_name="image",
            index=models.Index(
                fields=["-total_likes"], name="images_imag_total_l_0bcd7e_idx"
            ),
        ),
    ]
