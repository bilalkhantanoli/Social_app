"""
This module contains the configuration for the 'feed' app.
It defines the FeedConfig class to configure the app within Django.
"""

from django.apps import AppConfig

class FeedConfig(AppConfig):
    """
    Configuration class for the 'feed' app.
    This class sets the default_auto_field and the name of the app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feed'

    def ready(self):
        import feed.signals
