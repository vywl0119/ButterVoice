# Create your models here.
from unicodedata import category
from django.db import models

# Create your models here.

class customer(models.Model):
    cu_id = models.CharField(max_length=45, null=False, primary_key=True)
    pw = models.CharField(max_length=45, null=False)
    name = models.CharField(max_length=45, null=False)
    phone = models.CharField(max_length=45, null=False)
    profile = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'customer'
        managed = False


class counselor(models.Model):
    co_id = models.CharField(max_length=45, null=False, primary_key=True)
    pw = models.CharField(max_length=45, null=False)
    category = models.CharField(max_length=45, null=False)
    name = models.CharField(max_length=45, null=False)
    phone = models.CharField(max_length=45, null=False)
    profile = models.CharField(max_length=100, null=True)
    onoff = models.CharField(max_length=45, null=False, default='OFF')

    class Meta:
        db_table = 'counselor'
        managed = False

class colling(models.Model):
    c_no = models.AutoField(primary_key=True)
    cu_id = models.OneToOneField('customer',  on_delete=models.CASCADE, db_column='cu_id')
    co_id = models.ForeignKey('counselor',  on_delete=models.CASCADE, db_column='co_id')
    current = models.CharField(max_length=45, null=False, default='대기')
    call_date = models.DateTimeField(null=False, auto_now_add=True)
    category = models.CharField(max_length=45, null=True)
    title = models.CharField(max_length=100, null=True)
    content = models.CharField(max_length=500, null=True)

    class Meta:
        db_table = 'colling'
        managed = False


class point(models.Model):
    star_id = models.AutoField(primary_key=True) 
    co_id = models.ForeignKey('counselor', on_delete=models.CASCADE, db_column='co_id')
    star = models.IntegerField(null=False)

    class Meta:
        db_table = 'point'
        managed = False


        
