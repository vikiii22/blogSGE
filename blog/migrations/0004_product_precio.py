# Generated by Django 3.2.9 on 2022-02-25 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_rename_post_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='precio',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]