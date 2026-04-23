from utils import database_utils as database
from utils import process_utils as process
from utils import memory_utils as memory
from utils import alert_utils as alert
from utils import auth_utils as auth
from utils import disk_utils as disk
from utils import json_utils as json
from utils import log_utils as log
from utils import sys_utils as sys
from datetime import datetime

def get_time():
    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return now