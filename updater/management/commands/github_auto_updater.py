import time
import logging
from django.core.management.base import BaseCommand, CommandError
from updater.utils import perform_update, is_update_available

logger = logging.getLogger("updater.poller")

class Command(BaseCommand):
    help = "Polls GitHub for updates and applies them automatically."

    def add_arguments(self, parser):
        parser.add_argument('--interval', type=int, default=60, help="Interval in seconds between update checks.")

    def handle(self, *args, **options):
        interval = options['interval']
        self.stdout.write(self.style.SUCCESS(f"Starting GitHub auto-updater (interval: {interval}s)..."))
        while True:
            try:
                if is_update_available():
                    self.stdout.write("Update available. Applying update...")
                    perform_update()  # This will restart process if successful
                else:
                    self.stdout.write("No update available.")
            except Exception as e:
                logger.error(f"Updater exception: {e}")
                self.stderr.write(f"Error during update: {e}")
            time.sleep(interval)