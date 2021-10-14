from django.contrib import admin
from .models import GameDemo, GameCharacter, CharacterPosture


class GameDemoAdmin(admin.ModelAdmin):
    list_display = ["pk", "title"]


class GameCharacterAdmin(admin.ModelAdmin):
    list_display = ["pk", "game", "name"]


class CharacterPostureAdmin(admin.ModelAdmin):
    list_display = ["pk", "character", "name"]


# Register your models here.
admin.site.register(GameDemo, GameDemoAdmin)
admin.site.register(GameCharacter, GameCharacterAdmin)
admin.site.register(CharacterPosture, CharacterPostureAdmin)
