from optparse import make_option

from django.conf import settings
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.management.commands.runserver import BaseRunserverCommand

from django_gears.handlers import AssetFilesHandler


class Command(BaseRunserverCommand):

    option_list = BaseRunserverCommand.option_list + (
        make_option('--noassets', action='store_false',
                    dest='use_assets_handler', default=True,
                    help='Tells Django to NOT automatically serve asset files '
                         'at STATIC_URL.'),
        make_option('--nostatic', action='store_false',
                    dest='use_static_handler', default=True,
                    help='Tells Django to NOT automatically serve static '
                         'files at STATIC_URL.'),
        make_option('--insecure', action='store_true', dest='insecure_serving',
                    default=False, help='Allows serving static files even if '
                                        'DEBUG is False'),
    )
    help = ('Starts a lightweight Web server for development and also serves '
            'static files.')

    def get_handler(self, *args, **options):
        handler = super(Command, self).get_handler(*args, **options)
        use_assets_handler = options.get('use_assets_handler', True)
        use_static_handler = options.get('use_static_handler', True)
        insecure_serving = options.get('insecure_serving', False)
        

        if use_static_handler and (settings.DEBUG or insecure_serving):
            if use_assets_handler:
                return AssetFilesHandler(handler)
            return StaticFilesHandler(handler)
        return handler
