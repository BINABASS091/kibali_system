from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='KibaliUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('officer', 'Officer')], default='officer', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Permit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permit_number', models.CharField(max_length=20, unique=True)),
                ('jina', models.CharField(max_length=255)),
                ('aina', models.CharField(choices=[('UKUTA', 'Ukuta (Wall)'), ('NYUMBA', 'Nyumba (House)'), ('JENGO', 'Jengo (Building)'), ('KIWANDA', 'Kiwanda (Factory)'), ('DUKA', 'Duka (Shop)'), ('OFISI', 'Ofisi (Office)')], max_length=50)),
                ('pahala', models.CharField(max_length=255)),
                ('shehia', models.CharField(max_length=255)),
                ('kaskazini', models.CharField(max_length=255)),
                ('mashariki', models.CharField(max_length=255)),
                ('magharibi', models.CharField(max_length=255)),
                ('kusini', models.CharField(max_length=255)),
                ('upana', models.FloatField()),
                ('urefu', models.FloatField()),
                ('tarehe_kutolewa', models.DateField(auto_now_add=True)),
                ('tarehe_mwisho', models.DateField()),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='permits/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
