from api import app
from config import conf
from database_manager import init_db
from logger import logger


@app.on_event('startup')
def on_startup():
    logger.info("App started")


def main():
    if not conf.testing:
        init_db(app)


if __name__ == "main":
    main()


if __name__ == '__main__':
    logger.critical("Program started as __main__")
    