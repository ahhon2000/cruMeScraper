from collections import OrderedDict

from django.shortcuts import render
from django.views.generic import TemplateView

from lposts.models import Post

class LatestPostsView(TemplateView):
    template_name = 'lposts/latest_posts.html'

    def get_context_data(self, **kwarg):
        ctx = super().get_context_data(**kwarg)
        ts = OrderedDict(map(
            lambda x: (x[0], x[1].order_by('-article_date', 'title')),
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
        })

        return ctx
