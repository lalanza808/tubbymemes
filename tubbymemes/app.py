from logging.config import dictConfig

from tubbymemes.factory import create_app
from tubbymemes import config


app = create_app()

dictConfig(config.LOGGING_CONFIG)

if __name__ == '__main__':
    app.run()
