from django.contrib import admin

# Register your models here.
from .models import PLAN, INCOMESOURCE, USER

admin.site.register(USER)
admin.site.register(PLAN)
admin.site.register(INCOMESOURCE)