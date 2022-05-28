import logging

logger = logging.getLogger(__name__)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("error.log")
file_handler.setLevel(logging.ERROR)

sh_formatter = logging.Formatter(
  "%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s"
)
stream_handler.setFormatter(sh_formatter)

fh_formatter = logging.Formatter(
  "%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s"
)
file_handler.setFormatter(fh_formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

