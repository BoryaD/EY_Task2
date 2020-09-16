from django.db import models

# Create your models here.

from django.db import models


class File(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='files')

    def __str__(self):
        return self.title


class ClassType(models.Model):
    description = models.CharField(max_length=255)
    file = models.ForeignKey(File, on_delete=models.CASCADE, default='0', editable=False)


class Bill(models.Model):
    num = models.CharField(max_length=5)
    file = models.ForeignKey(File, on_delete=models.CASCADE, default='0', editable=False)
    class_of = models.ForeignKey(ClassType, on_delete=models.CASCADE, default='0')


class GroupBill(models.Model):
    parent_num = models.ForeignKey(Bill, on_delete=models.CASCADE)
    num_group = models.CharField(max_length=5)
    file = models.ForeignKey(File, on_delete=models.CASCADE, default='0', editable=False)


class IncomingBalance(models.Model):
    full_bill = models.ForeignKey(GroupBill, on_delete=models.CASCADE)
    active = models.FloatField()
    passive = models.FloatField()
    file = models.ForeignKey(File, on_delete=models.CASCADE, default='0', editable=False)


class OutcomingBalance(models.Model):
    full_bill = models.ForeignKey(GroupBill, on_delete=models.CASCADE)
    active = models.FloatField()
    passive = models.FloatField()
    file = models.ForeignKey(File, on_delete=models.CASCADE, default='0', editable=False)


class Turnover(models.Model):
    full_bill = models.ForeignKey(GroupBill, on_delete=models.CASCADE)
    debet = models.FloatField()
    credit = models.FloatField()
    file = models.ForeignKey(File, on_delete=models.CASCADE, default='0', editable=False)
