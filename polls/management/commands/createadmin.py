from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            print('Creating superuser...')
            admin = User.objects.create_superuser(
                email='superuser@fabrique.com',
                username='su',
                password='101010'
            )
            admin.is_active = True
            admin.save()
        else:
            print('Superuser exists.')