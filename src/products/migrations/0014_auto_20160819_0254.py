# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage
import products.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0013_myproducts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('media', models.ImageField(storage=django.core.files.storage.FileSystemStorage(location=b'/Users/davidrodgers/Desktop/Stuff/ecommerce/static_cdn/protected'), width_field=b'width', height_field=b'height', upload_to=products.models.download_media_location, blank=True, null=True)),
                ('height', models.CharField(max_length=20, null=True, blank=True)),
                ('width', models.CharField(max_length=20, null=True, blank=True)),
                ('product', models.ForeignKey(to='products.Product')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='myproducts',
            options={'verbose_name': 'My Products', 'verbose_name_plural': 'My Products'},
        ),
    ]
