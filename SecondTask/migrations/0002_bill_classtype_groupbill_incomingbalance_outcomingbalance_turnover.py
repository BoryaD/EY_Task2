# Generated by Django 3.1.1 on 2020-09-15 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SecondTask', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ClassType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='GroupBill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_group', models.IntegerField()),
                ('parent_num', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SecondTask.bill')),
            ],
        ),
        migrations.CreateModel(
            name='Turnover',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debet', models.BigIntegerField()),
                ('credit', models.BigIntegerField()),
                ('bill_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SecondTask.bill')),
                ('class_of', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SecondTask.classtype')),
                ('full_bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SecondTask.groupbill')),
            ],
        ),
        migrations.CreateModel(
            name='OutcomingBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BigIntegerField()),
                ('passive', models.BigIntegerField()),
                ('bill_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SecondTask.bill')),
                ('class_of', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SecondTask.classtype')),
                ('full_bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SecondTask.groupbill')),
            ],
        ),
        migrations.CreateModel(
            name='IncomingBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BigIntegerField()),
                ('passive', models.BigIntegerField()),
                ('bill_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SecondTask.bill')),
                ('class_of', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SecondTask.classtype')),
                ('full_bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SecondTask.groupbill')),
            ],
        ),
    ]
