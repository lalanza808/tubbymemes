from huey import RedisHuey

from tubbymemes.factory import create_app_huey
from tubbymemes import config


huey = RedisHuey(
    host=config.CACHE_HOST,
    port=config.CACHE_PORT
)

app = create_app_huey()
