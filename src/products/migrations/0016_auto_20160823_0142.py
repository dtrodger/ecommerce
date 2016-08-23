# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20160819_2129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thumbnail',
            name='user',
        ),
        migrations.AddField(
            model_name='thumbnail',
            name='type',
            field=models.CharField(default=b'hd', max_length=20, choices=[(b'hd', b'HD'), (b'sd', b'SD'), (b'micro', b'Micro')]),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='media',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location=b'/Users/davidrodgers/Desktop/Stuff/ecommerce/static_cdn/protected'), null=True, upload_to=products.models.download_media_location, blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=30),
        ),
    ]
