from logging.config import dictConfig

from suchwowx.factory import create_app
from suchwowx import config


app = create_app()

dictConfig(config.LOGGING_CONFIG)

if __name__ == '__main__':
    app.run()
