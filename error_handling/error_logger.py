import logging

def log_error(error_message):
    logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.error(error_message)
