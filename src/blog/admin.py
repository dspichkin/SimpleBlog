#coding: utf-8
from django.contrib import admin
from blog.models import Tag, Category, Post, PostImage


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'weight')
    list_display_links = ('id', 'name')
    prepopulated_fields = {"slug": ("name",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')
    list_display_links = ('id', 'name')


class PostImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'imagepath')
    list_display_links = ('id', 'post')
    #readonly_fields = ("get_url",)


class PostImageInline(admin.TabularInline):

    model = PostImage
    extra = 1
    classes = ('grp-collapse grp-closed',)
    inline_classes = ('grp-collapse grp-closed',)
    readonly_fields = ('url',)
    fieldsets = (
        (None, {'fields': ('post', 'imagepath', 'url')}),
    )


class PostAdmin(admin.ModelAdmin):
    #class Media:
    #    js = (
    #        '/static/js/tinymce/tinymce.min.js',
    #        '/static/js/tinymce/tinymce_init.js',
    #    )
    change_form_template = 'blog/admin/change_form.html'
    list_display = ('id', 'title', 'is_public', 'is_removed', 'modified', 'allow_comments')
    list_display_links = ('id', 'title')
    prepopulated_fields = {"slug": ("title",)}
    inlines = (PostImageInline, )

    fieldsets = (
        (None, {'fields': ('title', 'slug', 'parent', 'order')}),
        (u'Тело заметки', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('body', )
        }),
        (u'Категории', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('category', 'tags')
        }),
        (u'Публикация', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('is_public', 'is_removed')
        }),
        (u'Дополнительные параметры', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('allow_comments', 'related_posts', 'meta_keywords', 'meta_description')
        }),
    )


admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostImage, PostImageAdmin)
