# Generated by Django 3.2.6 on 2021-11-10 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='cardNumber',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='cvv',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='expiration',
            field=models.CharField(max_length=5, null=True),
        ),
    ]
