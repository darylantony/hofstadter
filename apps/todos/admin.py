from django.contrib import admin
from django.db.models import get_model
from todos.forms import ToDoAdminModelForm
from todos.models import *


# Inlines

class ToDoListInline(admin.TabularInline):
    model = get_model('todos', 'todolist')
    extra = 0
    
class ToDoInline(admin.TabularInline):
    model = get_model('todos', 'todo')
    extra = 0
    
class TimingInline(admin.TabularInline):
    model = get_model('todos', 'timing')
    extra = 0
    
# Classes

admin.site.register(get_model('todos', 'category'))

class ToDoListAdmin(admin.ModelAdmin):
    
    form = ToDoAdminModelForm
    
    list_display = (
        'title',
        'description',
        'milestone',
        'timed',
        'guesstimated',)
    
    list_filter = (
        'milestone',)

    inlines = [
        ToDoInline,]

admin.site.register(get_model('todos', 'todolist'), ToDoListAdmin)

class ToDoAdmin(admin.ModelAdmin):

    list_display = (
        'task',
        'todo_list',
        'responsible',
        'timed',
        'guesstimated',
        'due',
        'done',)
    
    list_editable = (
        'responsible',
        'due',
        'done',)
    
    list_filter = (
        'todo_list',
        'done',)

    inlines = [
        TimingInline]

admin.site.register(get_model('todos', 'todo'), ToDoAdmin)


# class GuesstimateAdmin(admin.ModelAdmin):
#     list_display = (
#         'timing',
#         'duration',
#         'timed',
#         'remaining',
#         'overtime'
#     )
#     
#     list_editable = (
#         'duration',
#     )
#     
#     
# admin.site.register(get_model('todos', 'guesstimate'), GuesstimateAdmin)

class TimingAdmin(admin.ModelAdmin):
    
    # date_hierarchy = 'start'
    
    list_display = (
        'todo',
        'start',
        'stop',
        'duration',
        'notes',
    )
    
    list_editable = (
        'start',
        'stop',
    )
    
    list_filter = (
        'start',
    )
    
admin.site.register(get_model('todos', 'timing'), TimingAdmin)