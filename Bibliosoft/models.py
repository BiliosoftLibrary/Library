# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class book(models.Model):
    name = models.CharField(max_length=32)
    id = models.AutoField(max_length=32, primary_key=True)
    floor = models.CharField(max_length=32)
    shelf = models.CharField(max_length=32)
    area = models.CharField(max_length=32)
    price = models.CharField(max_length=32)
    ISBN = models.CharField(max_length=32)
    category = models.CharField(max_length=32)
    islent = models.CharField(max_length=32, default='0')

class librarian(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    pwd = models.CharField(max_length=32, default='00010001')
    isrequest = models.CharField(max_length=32, default='0')

class admin(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    pwd = models.CharField(max_length=32)

class reader(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    pwd = models.CharField(max_length=32, default='12345678')
    email = models.CharField(max_length=32)
    sex = models.CharField(max_length=32)
    deposit = models.CharField(max_length=32)

class lend(models.Model):
    list_id = models.AutoField(max_length=32, primary_key=True)
    book_id = models.CharField(max_length=32)
    book_name = models.CharField(max_length=32)
    reader_id = models.CharField(max_length=32)
    remain_lendingtime = models.CharField(max_length=32, default='0')
    isreturned = models.CharField(max_length=32)
    date = models.CharField(max_length=32)

class category(models.Model):
    name = models.CharField(max_length=32)

class default(models.Model):
    fine = models.CharField(max_length=32)
    return_period = models.CharField(max_length=32)
    deposit = models.CharField(max_length=32)
    post = models.CharField(max_length=32)

class appointment(models.Model):
    reader_id = models.CharField(max_length=32)
    book_id = models.CharField(max_length=32)
    book_name = models.CharField(max_length=32)
    time = models.CharField(max_length=32)

class delete(models.Model):
    book_id = models.CharField(max_length=32, primary_key=True)
    book_name = models.CharField(max_length=32)
    librarian_id = models.CharField(max_length=32)

class fine(models.Model):
    list_id = models.AutoField(max_length=32, primary_key=True)
    book_name = models.CharField(max_length=32)
    reader_id = models.CharField(max_length=32)
    date = models.CharField(max_length=32)
    ispayed = models.CharField(max_length=32, default='0')
    topay_fine = models.CharField(max_length=32, default='0')

class income(models.Model):
    date = models.CharField(max_length=32)
    deposit = models.CharField(max_length=32)
    fine = models.CharField(max_length=32)
    sum = models.CharField(max_length=32)