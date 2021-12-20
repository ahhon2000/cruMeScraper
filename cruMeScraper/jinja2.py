from jinja2 import Environment
from django.urls import reverse
from django.contrib.staticfiles.storage import staticfiles_storage
# for more later django installations use:
#from django.templatetags.static import static

def staticLinkMaker(prefix):
    return lambda s: staticfiles_storage.url(f'{prefix}{s}')

def environment(**options):
	env = Environment(**options)
	env.globals.update({
		"static": staticfiles_storage.url,
		#"static": static,
		"url": reverse,
        #"bootstrap": lambda s: static(f"bootstrap/{s}"),
        #"bootstrap": lambda s: staticfiles_storage.url(f"bootstrap/{s}"),
	})
	return env
