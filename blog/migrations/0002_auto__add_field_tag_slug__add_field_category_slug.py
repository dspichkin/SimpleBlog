# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Tag.slug'
        db.add_column(u'blog_tag', 'slug',
                      self.gf('django.db.models.fields.SlugField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Category.slug'
        db.add_column(u'blog_category', 'slug',
                      self.gf('django.db.models.fields.SlugField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Tag.slug'
        db.delete_column(u'blog_tag', 'slug')

        # Deleting field 'Category.slug'
        db.delete_column(u'blog_category', 'slug')


    models = {
        u'blog.category': {
            'Meta': {'ordering': "['order_id', 'name']", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order_id': ('django.db.models.fields.SmallIntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'blog.post': {
            'Meta': {'ordering': "('-modified',)", 'object_name': 'Post'},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blog.Category']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'related_posts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_posts_rel_+'", 'blank': 'True', 'to': u"orm['blog.Post']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'tags'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['blog.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'blog.tag': {
            'Meta': {'ordering': "['name']", 'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['blog']