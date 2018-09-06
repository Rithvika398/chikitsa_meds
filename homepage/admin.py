from django.contrib import admin
from .models import Medicines,Doctor,Appt,Order,Cart,Product,Variation,VariationManager
# Register your models here.
admin.site.register(Medicines)
admin.site.register(Doctor)
admin.site.register(Appt)
admin.site.register(Cart)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Variation)
#admin.site.register(VariationManager)






