from django.contrib import admin
from . import models

admin.site.register(models.MenuItem)
admin.site.register(models.OrderItem)
admin.site.register(models.Category)
admin.site.register(models.Cart)
admin.site.register(models.Order)

# Register your models here.
