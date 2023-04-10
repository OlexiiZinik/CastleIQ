from config import conf
from logger import logger

import uvicorn
import os

if __name__ == '__main__':
    logger.info("Program started using runner.py")
    os.putenv('TIMEZONE', conf.timezone)
    uvicorn.run(
        "main:app",
        host=conf.host,
        port=conf.port,
        reload=conf.debug and conf.reload,
        use_colors=True
    )