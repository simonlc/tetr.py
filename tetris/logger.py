import logging
logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)
