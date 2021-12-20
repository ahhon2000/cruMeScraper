from collections import OrderedDict

from django.shortcuts import render
from django.views.generic import TemplateView

from lposts.models import Post

class LatestPostsView(TemplateView):
    template_name = 'lposts/latest_posts.html'

    def get_context_data(self, **kwarg):
        ctx = super().get_context_data(**kwarg)
        ctx.update({
            'tables': OrderedDict((
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
            )),
        })

        return ctx
