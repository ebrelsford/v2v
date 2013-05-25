from django import template
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from classytags.arguments import Argument
from classytags.core import Options, Tag

register = template.Library()

class TweetButton(Tag):
    name = 'tweet_button'
    options = Options(
        Argument('text'),
        'link_to',
        Argument('obj', required=False),
    )

    def render_tag(self, context, text, obj):
        return render_to_string('twitter/tweet_button.html', {
            'BASE_URL': Site.objects.get_current().domain,
            'text': text,
            'obj': obj,
        })

register.tag(TweetButton)
