# Generated by Django 4.1 on 2022-08-24 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0005_alter_cart_item_cart"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="id",
            field=models.UUIDField(primary_key=True, serialize=False),
        ),
    ]