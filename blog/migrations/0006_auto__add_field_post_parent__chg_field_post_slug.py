# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Post.parent'
        db.add_column(u'blog_post', 'parent',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['blog.Post']),
                      keep_default=False)


        # Changing field 'Post.slug'
        db.alter_column(u'blog_post', 'slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50))

    def backwards(self, orm):
        # Deleting field 'Post.parent'
        db.delete_column(u'blog_post', 'parent_id')


        # Changing field 'Post.slug'
        db.alter_column(u'blog_post', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=100, unique=True))

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
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['blog.Post']"}),
            'related_posts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'related_posts_rel_+'", 'blank': 'True', 'to': u"orm['blog.Post']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'tags'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['blog.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'blog.postimage': {
            'Meta': {'ordering': "['id']", 'object_name': 'PostImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagepath': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['blog.Post']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
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