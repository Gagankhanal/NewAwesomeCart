# Generated by Django 3.2 on 2021-04-30 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=600)),
                ('publish_date', models.DateField()),
            ],
        ),
    ]
