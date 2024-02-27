import logging

from config import CUSTOM_LOGGING, LOG_LEVEL

# print(SYSINFO, WARN, ERROR, SUCCESS)
logging.addLevelName(CUSTOM_LOGGING.DEBUG, 'DEBUG')
logging.addLevelName(CUSTOM_LOGGING.INFO, 'INFO ')
logging.addLevelName(CUSTOM_LOGGING.WARN, 'WARN ')
logging.addLevelName(CUSTOM_LOGGING.ERROR, 'ERROR')
logging.addLevelName(CUSTOM_LOGGING.CRITICAL, 'CRITICAL')


logger = logging.getLogger('LOGGER')

try:
    from lib.ansistrm import ColorizingStreamHandler
    handle = ColorizingStreamHandler()
except Exception as e:
    print(e)
    handle = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - [%(levelname)s]  %(message)s', '%Y/%m/%d %H:%M:%S')
handle.setFormatter(formatter)
logger.addHandler(handle)
logger.setLevel(LOG_LEVEL)


class LOGGER:
    @staticmethod
    def info(msg, *args, **kwargs):
        return logger.log(CUSTOM_LOGGING.INFO, msg, *args, **kwargs)

    @staticmethod
    def warning(msg, *args, **kwargs):
        return logger.log(CUSTOM_LOGGING.WARN, msg, *args, **kwargs)

    @staticmethod
    def error(msg, *args, **kwargs):
        return logger.log(CUSTOM_LOGGING.ERROR, msg, *args, **kwargs)

    @staticmethod
    def debug(msg, *args, **kwargs):
        return logger.log(CUSTOM_LOGGING.DEBUG, msg, *args, **kwargs)
    
    @staticmethod
    def critical(msg, *args, **kwargs):
        return logger.log(CUSTOM_LOGGING.CRITICAL, msg, *args, **kwargs)