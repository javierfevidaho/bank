from django.core.management.base import BaseCommand
from django.db import models
from core.models import Ticket

class Command(BaseCommand):
    help = 'Remove duplicate tickets'

    def handle(self, *args, **kwargs):
        duplicates = (
            Ticket.objects.values('user', 'numbers', 'bonus')
            .annotate(max_id=models.Max('id'), count_id=models.Count('id'))
            .filter(count_id__gt=1)
        )

        for duplicate in duplicates:
            (
                Ticket.objects
                .filter(user=duplicate['user'], numbers=duplicate['numbers'], bonus=duplicate['bonus'])
                .exclude(id=duplicate['max_id'])
                .delete()
            )

        self.stdout.write(self.style.SUCCESS('Successfully removed duplicate tickets'))
