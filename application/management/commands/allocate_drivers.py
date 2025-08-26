from django.core.management.base import BaseCommand
from application.utils import allocate_drivers
import time

"""This class is for allocating drivers to rides automatically by searching their availability in location"""
class Command(BaseCommand):
    help = 'Periodically allocate drivers to rides'

    def handle(self, *args, **kwargs):
        while True:
            allocate_drivers()
            time.sleep(10)