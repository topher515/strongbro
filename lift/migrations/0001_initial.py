# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ExerciseData'
        db.create_table(u'lift_exercisedata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('definition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lift.ExerciseDef'])),
            ('ts', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('previous', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='next', unique=True, null=True, to=orm['lift.ExerciseData'])),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('data', self.gf('jsonfield.fields.JSONField')()),
        ))
        db.send_create_signal(u'lift', ['ExerciseData'])

        # Adding model 'ExerciseDef'
        db.create_table(u'lift_exercisedef', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('video_url', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('algorithm', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('options', self.gf('jsonfield.fields.JSONField')()),
        ))
        db.send_create_signal(u'lift', ['ExerciseDef'])


    def backwards(self, orm):
        # Deleting model 'ExerciseData'
        db.delete_table(u'lift_exercisedata')

        # Deleting model 'ExerciseDef'
        db.delete_table(u'lift_exercisedef')


    models = {
        u'lift.exercisedata': {
            'Meta': {'object_name': 'ExerciseData'},
            'data': ('jsonfield.fields.JSONField', [], {}),
            'definition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lift.ExerciseDef']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'previous': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'next'", 'unique': 'True', 'null': 'True', 'to': u"orm['lift.ExerciseData']"}),
            'ts': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'})
        },
        u'lift.exercisedef': {
            'Meta': {'object_name': 'ExerciseDef'},
            'algorithm': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'options': ('jsonfield.fields.JSONField', [], {}),
            'video_url': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }

    complete_apps = ['lift']