from collections import OrderedDict

from django.shortcuts import render
from django.views.generic import TemplateView

from cruMeScraper.settings import LPOSTS
from lposts.models import Post
from cruMeScraper.jinja2 import staticLinkMaker

class LatestPostsView(TemplateView):
    template_name = 'lposts/latest_posts.html'

    def get_context_data(self, **kwarg):
        app_name = 'lposts'
        ctx = super().get_context_data(**kwarg)
        N = LPOSTS['N_POSTS']
        ts = OrderedDict(map(
            lambda x: (
                x[0],
                x[1].order_by('-article_date', 'title')[0:N],
            ),
            (
                (
                    'TechCrunch & Medium',
                    Post.objects.all(),
                ), (
                    'TechCrunch',
                    Post.objects.filter(source='TC'),
                ), (
                    'Medium',
                    Post.objects.filter(source='ME'),
                ),
            ),
        ))
        ctx.update({
            'tables': ts,
            'fmtDate': lambda d: d.strftime("%Y-%m-%d %H:%M:%S"),
            'appStatic': staticLinkMaker(f'{app_name}/'),
            'fmtExcerpt': lambda e: \
                    e + '...' if e and not e[-1] in "!?." else e,
            'enumerate': enumerate,
        })

        return ctx
