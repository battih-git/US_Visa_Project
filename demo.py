from US_VISA_PROJECT.logger import logging
from US_VISA_PROJECT.exception import USvisaException
import sys

logging.info('Welcome to our customer log')

try:
    a = 2/0
except Exception as e:
    raise USvisaException(e, sys)