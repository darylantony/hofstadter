from django.contrib import admin
from django.db.models import get_model

from todos.admin import ToDoListInline

class MilestoneAdmin(admin.ModelAdmin):
    
    list_display = (
        'title',
        'due',
        'responsible',
        'timed',
        'guesstimated',
    )
    
    list_editable = (
        'due',
        'responsible',
    )
    
    inlines = [
        ToDoListInline,
    ]

admin.site.register(get_model('milestones', 'milestone'), MilestoneAdmin)