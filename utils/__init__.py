from utils import process_utils as process_u
from utils import memory_utils as memory_u
from utils import alert_utils as alert_u
from utils import disk_utils as disk_u
from utils import json_utils as json_u
from utils import log_utils as log_u
from utils import sys_utils as sys_u
from utils import ip_utils as ip_u
from datetime import datetime

def get_time():
    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return now