# Generated by Django 5.1.3 on 2024-11-10 16:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('iban', models.CharField(max_length=34)),
                ('total_investment', models.DecimalField(decimal_places=2, max_digits=15)),
                ('investment_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='CapitalCall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('status', models.CharField(choices=[('validated', 'Validated'), ('sent', 'Sent'), ('paid', 'Paid'), ('overdue', 'Overdue')], max_length=10)),
                ('due_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('investor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='capital_call_app.investor')),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bill_type', models.CharField(choices=[('membership', 'Membership'), ('upfront_fee', 'Upfront Fee'), ('yearly_fee', 'Yearly Fee')], max_length=15)),
                ('generated_at', models.DateTimeField(auto_now_add=True)),
                ('capital_call', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bills', to='capital_call_app.capitalcall')),
                ('investor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='capital_call_app.investor')),
            ],
        ),
    ]
