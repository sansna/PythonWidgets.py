import logging

logging.basicConfig(filename="test.log", level=logging.INFO, format='%(asctime)s: %(levelname)s: %(filename)s:%(lineno)d: %(funcName)s')
logging.info("ok")
