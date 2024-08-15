from django.contrib import admin
from .models import WeatherData0
from .models import WeatherData1
from .models import DemandData0

admin.site.register(WeatherData0)
admin.site.register(WeatherData1)
admin.site.register(DemandData0)

# Register your models here.