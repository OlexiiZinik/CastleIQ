from api import app
from database_manager import *
from logger import logger


@app.on_event('startup')
def on_startup():
    logger.info("App started")


def main():
    pass
    

if __name__ == "main":
    main()


if __name__ == '__main__':
    logger.critical("Program started as __main__")
    