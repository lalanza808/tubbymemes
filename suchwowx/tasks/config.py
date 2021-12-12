from huey import RedisHuey

from suchwowx.factory import create_app_huey
from suchwowx import config


huey = RedisHuey(
    host=config.CACHE_HOST,
    port=config.CACHE_PORT
)

app = create_app_huey()
