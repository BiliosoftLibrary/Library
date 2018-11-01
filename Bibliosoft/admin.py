# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from Bibliosoft import models
admin.site.register(models.book)
admin.site.register(models.librarian)
admin.site.register(models.admin)
admin.site.register(models.reader)
admin.site.register(models.lend)
admin.site.register(models.category)
admin.site.register(models.default)
admin.site.register(models.appointment)
admin.site.register(models.delete)
admin.site.register(models.fine)
admin.site.register(models.income)