from django.contrib import admin
from .models import MyBabyDrawings

# Register your models here.


class MyBabyDrawingsAdmin(admin.ModelAdmin):
    list_display = [
        "order_id",
        "user_id",
        "game_id",
        "date_added",
        "confirm_status",
        "status",
    ]



admin.site.register(MyBabyDrawings, MyBabyDrawingsAdmin)
