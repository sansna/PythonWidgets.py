# Basic config for logging module to use
from logging import basicConfig, INFO, getLogger, ERROR
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler

log_file_name = "test.log"
thandler = TimedRotatingFileHandler(log_file_name, when="S", interval=10, backupCount=10)
thandler.suffix = "%Y-%m-%d"
shandler = RotatingFileHandler(log_file_name, maxBytes=1024, backupCount=1000)

def ConfigLogger(logger):
    logger.addHandler(thandler)
    logger.addHandler(shandler)

basicConfig(filename=log_file_name, level=ERROR, format='%(asctime)s: %(levelname)s: %(filename)s:%(lineno)d: %(funcName)s: %(message)s', handlers=[thandler, shandler])
logger = getLogger()
#ConfigLogger(logger)

def main():
    logger.info("ok")

if __name__ == '__main__':
    main()
