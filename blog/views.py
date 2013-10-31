#coding: utf-8
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404

from blog.models import Tag, Category, Post

from BeautifulSoup import BeautifulSoup
from HTMLParser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class BlogPaginator():

    paginated_by = 5

    def paginator(self, qs, page):

        if len(qs) > 0:
            pages = Paginator(qs, self.paginated_by)

            if page is None:
                page = 1

            page = int(page)

            if page > pages.num_pages:
                raise Http404

            qspage = pages.page(page)
            qs = qspage.object_list

            obj = {}

            if pages.num_pages < 5:
                cpage_range = pages.page_range
            else:
                if page <= 3:
                    cpage_range = pages.page_range[:page + 2]
                    obj['page_next_range'] = page + 2

                elif page >= pages.num_pages - 2:
                    cpage_range = pages.page_range[page - 3:]
                    obj['page_previous_range'] = page - 5
                    if obj['page_previous_range'] < 1:
                        obj['page_previous_range'] = 1
                else:
                    cpage_range = pages.page_range[page - 3:page + 2]
                    obj['page_next_range'] = page + 2
                    obj['page_previous_range'] = page - 5
                    if obj['page_previous_range'] < 1:
                        obj['page_previous_range'] = 1

            obj['page_range'] = cpage_range
            obj['page_previous'] = qspage.has_previous()
            if obj['page_previous']:
                obj['number_page_previous'] = page - 1
            obj['page_next'] = qspage.has_next()
            if obj['page_next']:
                obj['number_page_next'] = page + 1
            obj['page'] = page

            posts = []
            for p in qs:
                temp = {
                    'slug': p.slug,
                    'title': p.title,
                    'category': p.category,
                    'tags': p.tags,
                    'is_public': p.is_public,
                    'is_removed': p.is_removed,

                }
                html = BeautifulSoup(p.body[:400])
                temp['body'] = html.prettify()
                if len(p.body) > 400:
                    temp['is_more'] = True

                posts.append(temp)
            obj['posts'] = posts
            return obj


class Home(TemplateView, BlogPaginator):
    """
    """
    template_name = 'index.html'

    def get_context_data(self):

        page = self.request.GET.get('page')

        obj = {}
        obj['tags'] = Tag.objects.all()
        obj['categories'] = Category.objects.filter(is_active=True)
        if self.request.user.is_authenticated():
            obj['recent_post'] = Post.objects.filter(parent=None)[:10]
            obj['pageposts'] = self.paginator(Post.objects.all(), page)
        else:
            obj['recent_post'] = Post.objects.filter(is_public=True, is_removed=False, parent=None)[:10]
            obj['pageposts'] = self.paginator(Post.objects.filter(is_public=True, is_removed=False), page)

        return obj


class CategoryView(TemplateView, BlogPaginator):
    """
    """
    template_name = 'index.html'

    def get_context_data(self, category):
        category = self.kwargs.get('category')

        page = self.request.GET.get('page')
        obj = {}
        obj['tags'] = Tag.objects.all()
        obj['categories'] = Category.objects.filter(is_active=True)
        obj['recent_post'] = Post.objects.filter(is_public=True, is_removed=False, parent=None)[:10]
        obj['pageposts'] = self.paginator(Post.objects.filter(is_public=True, is_removed=False, category__slug=category), page)

        return obj


class TagView(TemplateView, BlogPaginator):
    """
    """
    template_name = 'index.html'

    def get_context_data(self, tag):
        tag = self.kwargs.get('tag')

        page = self.request.GET.get('page')
        obj = {}
        obj['tags'] = Tag.objects.all()
        obj['categories'] = Category.objects.filter(is_active=True)
        obj['recent_post'] = Post.objects.filter(is_public=True, is_removed=False, parent=None)[:10]
        obj['pageposts'] = self.paginator(Post.objects.filter(is_public=True, is_removed=False, tags__slug__in=[tag]), page)

        return obj


class PostView(TemplateView):
    """
    """
    template_name = 'post.html'

    def get_context_data(self, post):
        slug = self.kwargs.get('post')
        obj = {}
        obj['tags'] = Tag.objects.all()
        obj['categories'] = Category.objects.filter(is_active=True)

        if self.request.user.is_authenticated():
            obj['recent_post'] = Post.objects.filter(parent=None)[:10]
            obj['post'] = get_object_or_404(Post, slug=slug)
        else:
            obj['recent_post'] = Post.objects.filter(is_public=True, is_removed=False, parent=None)[:10]
            obj['post'] = get_object_or_404(Post, is_public=True, is_removed=False, slug=slug)

        if obj['post'].title:
            obj['meta_title'] = obj['post'].title + u" | Блог о веб разработке"
        else:
            obj['meta_title'] = u"Блог о веб разработке"

        if obj['post'].meta_keywords:
            obj['meta_keywords'] = obj['post'].meta_keywords
        else:
            obj['meta_keywords'] = obj['post'].title

        if obj['post'].meta_description:
            obj['meta_description'] = obj['post'].meta_description
        else:
            obj['meta_description'] = strip_tags(obj['post'].body[:400])

        return obj
