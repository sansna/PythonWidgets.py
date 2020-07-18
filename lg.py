import logging

logging.basicConfig(filename="test.log", level=logging.INFO, format='%(asctime)s: %(levelname)s: %(filename)s:%(lineno)d: %(funcName)s: %(message)s')

def main():
    logging.info("ok")

if __name__ == '__main__':
    main()
