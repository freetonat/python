import logging
import logging.handlers

logger = logging.getLogger("log")
logger.setLevel(logging.INFO)

formatter = logging.Formatter('[%(levelname)s[%(filename)s:%(lineno)s]%(asctime)s > %(message)s')

filehandler = logging.FileHandler('./my.log')
streamHandler = logging.StreamHandler()

filehandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

logger.addHandler(filehandler)
logger.addHandler(streamHandler)

logger.info('info haha')
