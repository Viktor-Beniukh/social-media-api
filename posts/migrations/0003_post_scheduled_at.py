# Generated by Django 4.2 on 2023-05-05 11:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0002_alter_hashtag_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="scheduled_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]