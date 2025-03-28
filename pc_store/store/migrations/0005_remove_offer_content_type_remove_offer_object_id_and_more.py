# Generated by Django 5.1.6 on 2025-03-13 18:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_offer_store'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='object_id',
        ),
        migrations.AddField(
            model_name='offer',
            name='case',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.case'),
        ),
        migrations.AddField(
            model_name='offer',
            name='graphic_card',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.graphiccard'),
        ),
        migrations.AddField(
            model_name='offer',
            name='motherboard',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.motherboard'),
        ),
        migrations.AddField(
            model_name='offer',
            name='power_supply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.powersupply'),
        ),
        migrations.AddField(
            model_name='offer',
            name='processor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.processor'),
        ),
        migrations.AddField(
            model_name='offer',
            name='ram',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.ram'),
        ),
        migrations.AddField(
            model_name='offer',
            name='storage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.storage'),
        ),
    ]
