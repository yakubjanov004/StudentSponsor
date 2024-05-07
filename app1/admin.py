from django.contrib import admin
from app1 import models

# Register your models here.


admin.site.register(models.Sponsor)
admin.site.register(models.University)
admin.site.register(models.Student)
admin.site.register(models.Student_Sponsor)
