# Generated by Django 4.0.4 on 2022-05-15 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_tag_updated_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='user_comment',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='parent_comment_id',
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.comment'),
        ),
    ]
