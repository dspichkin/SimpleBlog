# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Tag.slug'
        db.alter_column(u'blog_tag', 'slug', self.gf('django.db.models.fields.SlugField')(default=0, unique=True, max_length=100))
        # Adding unique constraint on 'Tag', fields ['slug']
        db.create_unique(u'blog_tag', ['slug'])


        # Changing field 'Category.slug'
        db.alter_column(u'blog_category', 'slug', self.gf('django.db.models.fields.SlugField')(default=0, unique=True, max_length=100))
        # Adding unique constraint on 'Category', fields ['slug']
        db.create_unique(u'blog_category', ['slug'])


    def backwards(self, orm):
        # Removing unique constraint on 'Category', fields ['slug']
        db.delete_unique(u'blog_category', ['slug'])

        # Removing unique constraint on 'Tag', fields ['slug']
        db.delete_unique(u'blog_tag', ['slug'])


        # Changing field 'Tag.slug'
        db.alter_column(u'blog_tag', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=100, null=True))

        # Changing field 'Category.slug'
        db.alter_column(u'blog_category', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=100, null=True))

    models = {
        u'blog.category': {
            'Meta': {'ordering': "['order_id', 'name']", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order_id': ('django.db.models.fields.SmallIntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
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
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['blog']