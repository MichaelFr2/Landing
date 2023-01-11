# Import smtplib for the actual sending function
from pysendpulse.pysendpulse import PySendPulse

REST_API_ID = ''
REST_API_SECRET = ''
TOKEN_STORAGE = 'memcached'
MEMCACHED_HOST = '127.0.0.1:11211'
SPApiProxy = PySendPulse(REST_API_ID, REST_API_SECRET, TOKEN_STORAGE, memcached_host=MEMCACHED_HOST)