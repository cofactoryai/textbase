import logging
import sys
from logging.handlers import RotatingFileHandler
import traceback

#add rolling logs file
# rolling_file_handler = RotatingFileHandler(
#     filename="logs/log_file.log",
#     maxBytes=25*1024*1024,
#     backupCount=25,
# )

logging.basicConfig(
level=logging.ERROR,
format='%(asctime)s: %(message)s',
datefmt="%Y-%m-%d %H:%M:%S",
handlers=[logging.StreamHandler(sys.stdout)]
)


#log are split into 3 categories info,warning,error
LOG_INFO = 'INFO'
LOG_WARNING = 'WARNING'
LOG_ERROR = 'ERROR'

def log_it(message, log_type):
    logging.error(f"{log_type} : {message}")
    if log_type == LOG_ERROR:
        logging.error(traceback.format_exc())
