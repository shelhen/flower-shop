# from django.templatetags.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment, Undefined
import logging


class SilentUndefined(Undefined):
    '''
    Dont break pageloads because vars arent there!
    '''
    def _fail_with_undefined_error(self, *args, **kwargs):
        logging.exception('JINJA2: something was undefined!')
        return None


def jinja2_environment(**options):
    env = Environment(**options)
    env.undefined = SilentUndefined
    env.globals.update({
        'static': staticfiles_storage.url,
        # 'static': static,
        'url': reverse,
    })
    return env




