# Generated by Django 4.1 on 2022-08-31 22:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("JoinUPTest", "0002_codeemail_codephone_user_email_validated_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="codeemail",
            name="user",
            field=models.ForeignKey(
                default=2,
                on_delete=django.db.models.deletion.CASCADE,
                to="JoinUPTest.user",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="codephone",
            name="user",
            field=models.ForeignKey(
                default=2,
                on_delete=django.db.models.deletion.CASCADE,
                to="JoinUPTest.user",
            ),
            preserve_default=False,
        ),
    ]
