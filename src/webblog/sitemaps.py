from django.contrib.sitemaps import Sitemap
from blog.models import Post


class indexSitemap(Sitemap):
    """Return the static sitemap items"""

    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Post.objects.filter(is_public=True, is_removed=False)

    def lastmod(self, obj):
        return obj.modified
