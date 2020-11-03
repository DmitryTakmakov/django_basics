# Generated by Django 2.2 on 2020-11-01 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('FM', 'формируется'), ('STP', 'отправлен в обработку'), ('PRD', 'обработан'), ('PD', 'оплачен'), ('RDY', 'готов к выдаче'), ('DN', 'выдан'), ('CNC', 'отменен')], default='FM', max_length=3, verbose_name='статус заказа'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Product', verbose_name='продукт'),
        ),
    ]
