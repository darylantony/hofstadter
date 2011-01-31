# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ToDoList'
        db.create_table('todos_todolist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('milestone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['milestones.Milestone'], null=True, blank=True)),
        ))
        db.send_create_signal('todos', ['ToDoList'])

        # Adding model 'ToDo'
        db.create_table('todos_todo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.TextField')()),
            ('todo_list', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['todos.ToDoList'])),
            ('responsible', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('due', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('done', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('todos', ['ToDo'])

        # Adding model 'Timing'
        db.create_table('todos_timing', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('todo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['todos.ToDo'])),
            ('is_estimate', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('stop', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('estimate', self.gf('django.db.models.fields.FloatField')()),
            ('duration', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('todos', ['Timing'])

        # Adding model 'Guesstimate'
        db.create_table('todos_guesstimate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timing', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['todos.Timing'], null=True, blank=True)),
            ('first', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('duration', self.gf('django.db.models.fields.FloatField')(default=1.0)),
        ))
        db.send_create_signal('todos', ['Guesstimate'])


    def backwards(self, orm):
        
        # Deleting model 'ToDoList'
        db.delete_table('todos_todolist')

        # Deleting model 'ToDo'
        db.delete_table('todos_todo')

        # Deleting model 'Timing'
        db.delete_table('todos_timing')

        # Deleting model 'Guesstimate'
        db.delete_table('todos_guesstimate')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'milestones.milestone': {
            'Meta': {'object_name': 'Milestone'},
            'due': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2011, 1, 30, 22, 45, 34, 902926)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'responsible': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'todos_milestone_responsible'", 'null': 'True', 'to': "orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'todos.guesstimate': {
            'Meta': {'object_name': 'Guesstimate'},
            'duration': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'first': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timing': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['todos.Timing']", 'null': 'True', 'blank': 'True'})
        },
        'todos.timing': {
            'Meta': {'object_name': 'Timing'},
            'duration': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'estimate': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_estimate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'stop': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'todo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['todos.ToDo']"})
        },
        'todos.todo': {
            'Meta': {'object_name': 'ToDo'},
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'due': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'responsible': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.TextField', [], {}),
            'todo_list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['todos.ToDoList']"})
        },
        'todos.todolist': {
            'Meta': {'object_name': 'ToDoList'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'milestone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['milestones.Milestone']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['todos']
