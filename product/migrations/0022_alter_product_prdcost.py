# Generated by Django 4.1.5 on 2023-02-08 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0021_product_prdis_active_alter_product_prdiimage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='PRDCost',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=5, null=True, verbose_name='Cost'),
        ),
    ]
