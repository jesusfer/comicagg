# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-21 13:54
from __future__ import unicode_literals

import comicagg.comics.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0002_rename_last_check'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comic',
            old_name='activo',
            new_name='active',
        ),
        migrations.RenameField(
            model_name='comic',
            old_name='noimages',
            new_name='no_images',
        ),
        migrations.AlterField(
            model_name='comic',
            name='active',
            field=models.BooleanField(default=False, help_text='The comic is ongoing and gets epdated regularly.', verbose_name='Is active?'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='no_images',
            field=models.BooleanField(default=False, help_text='Use it to hide the images of the comic, but allow a notification to the users.', verbose_name="Don't show images?"),
        ),
        migrations.AlterField(
            model_name='comic',
            name='backwards',
            field=models.BooleanField(default=False, help_text='Read the page backwards by line (last line first).', verbose_name='Check backwards.'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='backwards2',
            field=models.BooleanField(default=False, help_text='Read the page backwards by line (last line first).', verbose_name='Check backwards.'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='base2',
            field=models.CharField(blank=True, help_text='It must contain the placeholder <b>%s</b> which will be replaced with whatever matches in the regex.', max_length=255, null=True, verbose_name='Base URL for the page URL'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='base_img',
            field=models.CharField(blank=True, help_text='It must contain the placeholder <b>%s</b> which will be replaced with whatever matches in the regex.', max_length=255, null=True, verbose_name='Base URL for the image URL'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='custom_func',
            field=models.TextField(blank=True, help_text='Check the <a href="/docs/custom_func/">docs</a> for reference.', null=True, verbose_name='Custom update function'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='ended',
            field=models.BooleanField(default=False, help_text='Check this if the comic has ended. Also mark it as inactive.', verbose_name='Has ended?'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='fake_user_agent',
            field=models.BooleanField(default=False, help_text='Si además la web comprueba el User-Agent marcar para conectarse a la web usando otro User-Agent', verbose_name='Change User-Agent'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='last_image',
            field=models.URLField(blank=True, verbose_name='Last image URL'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='last_image_alt_text',
            field=comicagg.comics.fields.AltTextField(blank=True, null=True, verbose_name='Last image alt text'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='last_update',
            field=models.DateTimeField(blank=True, verbose_name='Last update'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='name',
            field=comicagg.comics.fields.ComicNameField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='notify',
            field=models.BooleanField(default=False, help_text="This is always disabled. If it's enabled when saving the comic, the users will be notified of the new comic.", verbose_name='Notify the users?'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Positive votes'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='referer',
            field=models.URLField(blank=True, help_text='Set this to a URL that the web will accept as referer when getting an update.', null=True, verbose_name='Referer'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='regexp',
            field=models.CharField(blank=True, help_text='It must contain one group (between parentheses) that matches the URL of the image.\n        Named groups can also be used:<br/>\n        - <i>url</i> for the URL of the image: (?P&lt;url>.+)<br/>\n        - <i>alt</i> for the alternative text of the image: (?P&lt;alt>.+)', max_length=255, null=True, verbose_name='Regular expression'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='regexp2',
            field=models.CharField(blank=True, help_text='It must contain one group (between parentheses) that matches the URL of the page.\n        Named groups can also be used:<br/>\n        - <i>url</i> for the URL of the page: (?P&lt;url>.+)', max_length=255, null=True, verbose_name='Regular expression'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='url',
            field=models.URLField(blank=True, help_text='If the redirection URL is used, this field will not be used.', null=True, verbose_name='URL of the page where the image can be found'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='url2',
            field=models.URLField(blank=True, help_text='Setting this enables the redirection. The engine will open this URL and\n        use the regex in this section to search for the URL of the page where the image can be found.', null=True, verbose_name='URL where the page of the image can be found'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='votes',
            field=models.IntegerField(default=0, verbose_name='Total votes'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='website',
            field=models.URLField(verbose_name='Website'),
        ),
        migrations.AlterField(
            model_name='comichistory',
            name='alt_text',
            field=comicagg.comics.fields.AltTextField(blank=True, null=True, verbose_name='Alternative text'),
        ),
    ]
