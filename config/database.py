import databases

from config.settings import get_settings

settings = get_settings()
database = databases.Database(settings.db_url)
