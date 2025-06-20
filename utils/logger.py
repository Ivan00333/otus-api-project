import logging


def get_logger(name: str) -> logging.Logger:
    """
    Создаёт и настраивает логгер с заданным именем,
    но добавляет хендлеры только один раз.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        fmt = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        date = "%Y-%m-%d %H:%M:%S"
        handler.setFormatter(logging.Formatter(fmt, datefmt=date))
        logger.addHandler(handler)

        logger.propagate = False

    return logger
