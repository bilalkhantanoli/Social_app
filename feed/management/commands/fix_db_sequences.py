from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management.color import no_style
from django.apps import apps

class Command(BaseCommand):
    help = "Fixes database sequences for all apps to resolve IntegrityError on ID fields"

    def handle(self, *args, **options):
        commands = []
        self.stdout.write("Generating sequence reset SQL...")
        
        for app_config in apps.get_app_configs():
            if not app_config.models_module:
                continue
            try:
                models = list(app_config.get_models())
                if not models:
                    continue
                    
                # sequence_reset_sql returns a list of SQL statements to reset sequences
                sql_list = connection.ops.sequence_reset_sql(no_style(), models)
                if sql_list:
                    commands.extend(sql_list)
                    self.stdout.write(f" - Found adjustments for {app_config.label}")
            except Exception as e:
                self.stderr.write(f"Error processing {app_config.label}: {e}")

        if commands:
            self.stdout.write(f"Executing {len(commands)} SQL commands...")
            with connection.cursor() as cursor:
                for sql in commands:
                    cursor.execute(sql)
            self.stdout.write(self.style.SUCCESS("Successfully reset database sequences for all apps."))
        else:
            self.stdout.write("No sequence reset commands were needed.")
