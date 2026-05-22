from django.core.management.base import BaseCommand
from django.urls import get_resolver


class Command(BaseCommand):
    help = 'Shows all URL patterns'

    def handle(self, *args, **options):
        resolver = get_resolver()
        self.show_urls(resolver)

    def show_urls(self, resolver, prefix=''):
        for pattern in resolver.url_patterns:
            if hasattr(pattern, 'url_patterns'):
                self.show_urls(pattern, prefix + str(pattern.pattern))
            else:
                self.stdout.write(f"{prefix}{pattern.pattern} -> {pattern.callback.__module__}.{pattern.callback.__name__}")