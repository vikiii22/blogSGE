# Generated by Django 3.2.9 on 2022-02-25 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_remove_product_precio'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='precio',
            field=models.FloatField(null=True),
        ),
    ]
