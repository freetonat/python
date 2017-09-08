#! /usr/bin/env python
__author__ ='eyonson'

import logging
import logging.handlers
import time

class TimeFormatter(object):

    # pylint: disable=W0232,R0201
    def format(self, record):
        print(record.getMessage())
        now = time.strftime("%H:%M:%S")
        return "{} {}".format(now, record.getMessage())

# 1. 로거 인스턴스를 만든다
logger = logging.getLogger('mylogger')

# 2. 스트림과 파일로 로그를 출력하는 핸들러를 각각 만든다.
fileHandler = logging.FileHandler('./myLoggerTest.log')
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(TimeFormatter())

# 3. 1번에서 만든 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
logger.addHandler(fileHandler)
logger.addHandler(streamHandler)

# 4. 로거 인스턴스로 로그를 찍는다.
logger.setLevel(logging.DEBUG)
logger.debug("===========================")
logger.info("TEST START")
logger.warning("스트림으로 로그가 남아요~")
logger.error("파일로도 남으니 안심이죠~!")
logger.critical("치명적인 버그는 꼭 파일로 남기기도 하고 메일로 발송하세요!")
logger.debug("===========================")
logger.info("TEST END!")
