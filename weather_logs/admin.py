from django.contrib import admin
from .models import State, Station, DailyTemp

# Register your models here.
admin.site.register(State)
admin.site.register(Station)
admin.site.register(DailyTemp)
