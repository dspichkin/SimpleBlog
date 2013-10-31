#coding: utf-8
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

import os
import random


class Tag(models.Model):
    name = models.CharField(max_length=50)
    weight = models.IntegerField(default=0)
    slug = models.SlugField(u'Slug', max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = u'Метки'

    def __unicode__(self):
        return u'%s - %s' % (self.name, self.weight)


class Category(models.Model):
    name = models.CharField(max_length=50)
    order_id = models.SmallIntegerField()
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(u'Slug', max_length=100, unique=True)

    class Meta:
        ordering = ['order_id', 'name']
        verbose_name_plural = u'Категории'

    def __unicode__(self):
        return u'%s: %s' % (self.id, self.name)


class Post(models.Model):
    title = models.CharField(u'Заголовок', max_length=255)
    slug = models.SlugField(u'Slug', max_length=50, unique=True)
    body = models.TextField(u'Тело статьи', blank=True, null=True)
    is_public = models.BooleanField(u'Опубликованно', default=True)
    is_removed = models.BooleanField(u'Удаленно', default=False)

    created = models.DateTimeField(u'Дата создания', auto_now_add=True)
    modified = models.DateTimeField(u'Дата модификации', auto_now=True)

    category = models.ForeignKey(Category, verbose_name=u'Категория', blank=True, null=True)
    tags = models.ManyToManyField(Tag, verbose_name=u'Метка', related_name=u'tags', blank=True, null=True)

    parent = models.ForeignKey(
        'self', related_name='children',
        null=True, blank=True,
        verbose_name=u"Родительская заметка",
    )
    order = models.SmallIntegerField(u"Позиция", blank=True, null=True)

    allow_comments = models.BooleanField(verbose_name=u"Позволить коментировать",
                                         default=True)

    related_posts = models.ManyToManyField(
        "self",
        verbose_name=u"Похожие посты", blank=True)

    meta_keywords = models.CharField(u"Meta keywords", max_length=255, blank=True, null=True)
    meta_description = models.CharField(u"Meta description", max_length=1024, blank=True, null=True)

    #admin_thumb_field = "featured_image"

    class Meta:
        verbose_name = u"Заметка"
        verbose_name_plural = u"Заметки"
        ordering = ("order", "-created",)

    def __unicode__(self):
        return u'%s: %s' % (self.id, self.title)

    def save(self, *args, **kwargs):
        if hasattr(self, 'tags'):
            self_id = None
            if hasattr(self, 'id'):
                self_id = self.id
            for t in self.tags.all():
                count = Post.objects.filter(tags__name=t.name).exclude(id=self_id).count()
                tag = Tag.objects.get(name=t.name)
                tag.weight = count + 1
                tag.save()

        return super(Post, self).save(*args, **kwargs)

    @property
    def get_child_posts(self):
        return Post.objects.filter(parent=self)

    def get_parents_posts(self):
        def get_parent(item, data):
            if item:
                temp = {}
                temp['id'] = item.id
                temp['title'] = item.name
                temp['slug'] = item.slug

                parent = item.get_parents_categories()
                if parent:
                    if len(parent) > 1:
                        parent.reverse()
                    temp['parent'] = parent

                data.append(temp)
                subitem = item.parent
                if subitem:
                    data = get_parent(subitem, data)
                return data

        data = []
        data = get_parent(self.parent, data)
        return data

    def get_absolute_url(self):
        return "/post/" + self.slug + '/'


def update_url(sender, instance, **kwargs):
    post_save.disconnect(update_url, sender=PostImage)
    filename = str(instance.imagepath).split('/')[-1]
    instance.url = settings.MEDIA_URL + 'images/' + str(instance.post.id) + "/" + filename
    instance.save()
    post_save.connect(update_url, sender=PostImage)


class PostImage(models.Model):

    def upload_to_by_id(self, filename):
        id = self.post.id
        if id:
            ext = filename[-3:]
            filename = self.post.slug + "." + str(ext)
            fullfilename = os.path.join(settings.PATH_POST_IMAGES, str(id), filename)

            return "%s" % fullfilename

    imagepath = models.ImageField(upload_to=upload_to_by_id)
    post = models.ForeignKey('Post', verbose_name=u"Заметка", blank=False, related_name="images")
    url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['id']
        verbose_name = u"Картинка"
        verbose_name_plural = u"Картинки"

    def __unicode__(self):
        return "%s %s" % (self.id, self.imagepath)

    def delete(self, *args, **kwargs):
        path = str(self.imagepath)
        if os.path.exists(path):
            os.remove(path)
        directory = os.path.join(settings.PATH_POST_IMAGES, str(self.post.id))
        if os.path.exists(directory):
            if not os.listdir(directory):
                os.rmdir(directory)
        super(PostImage, self).delete(*args, **kwargs)

post_save.connect(update_url, sender=PostImage)  # , dispatch_uid="update_url")
