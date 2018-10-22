from django.contrib import admin
from .models import Valve, Gate, Globe, Relief

# Register your models here.
admin.site.register(Valve)
admin.site.register(Gate)
admin.site.register(Globe)
admin.site.register(Relief)