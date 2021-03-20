# Generated by Django 3.1.7 on 2021-03-20 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client_Profile',
            fields=[
                ('profile_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=60)),
                ('date_of_birth', models.DateField(null=True)),
                ('contact_number', models.CharField(default='', max_length=30)),
                ('address', models.CharField(default='', max_length=100)),
                ('gender', models.CharField(default='', max_length=10)),
                ('bio', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Expert_Profile',
            fields=[
                ('profile_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=60)),
                ('date_of_birth', models.DateField(null=True)),
                ('contact_number', models.CharField(default='', max_length=30)),
                ('address', models.CharField(default='', max_length=100)),
                ('gender', models.CharField(default='', max_length=10)),
                ('bio', models.CharField(default='', max_length=200)),
                ('qualification', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('user_type', models.CharField(default='', max_length=100)),
                ('client_profile', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.client_profile')),
                ('expert_profile', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.expert_profile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(default='', max_length=300)),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
    ]
