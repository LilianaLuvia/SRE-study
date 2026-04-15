from utils import memory_utils
from utils import json_utils
from utils import log_utils
from utils import sys_utils
from utils import ip_utils
from datetime import datetime

def get_time():
    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return now