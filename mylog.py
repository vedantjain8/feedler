import logging

def logDef(loggLevel='info',logMSG=''):
    logging.basicConfig(filename=r"logs/logs.log",
                        encoding='utf-8',
                        format='%(asctime)s %(message)s',
                        filemode='a')

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if loggLevel.lower() =="info":
        logger.info(logMSG)
    elif loggLevel.lower() == "error":
        logger.error(logMSG)
    elif loggLevel.lower() == "debug":
        logger.debug(logMSG)