# Generated by Django 3.2.5 on 2021-12-20 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lposts', '0002_auto_20211220_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='source',
            field=models.CharField(choices=[('TC', 'TechCrunch'), ('ME', 'Medium')], default='TC', max_length=2),
            preserve_default=False,
        ),
    ]
