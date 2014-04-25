from django.contrib import admin
from sudoku.models import *

class MultiQuestAdmin(admin.ModelAdmin):
    list_display = ('questionTag', 'questionText', 'responseType', 'description', 'explanation')
    ordering = ('questionTag',)

# admin.site.register(Question, MultiQuestAdmin)  #register models for admin
# admin.site.register(ResponseChoice)
