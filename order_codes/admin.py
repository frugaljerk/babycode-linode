from django.contrib import admin
from .models import MyBabyCodes

# Register your models here.


class MyBabyCodesAdmin(admin.ModelAdmin):
    list_display = ["order_id", "user_id", "game_id", "date_added"]


admin.site.register(MyBabyCodes, MyBabyCodesAdmin)
