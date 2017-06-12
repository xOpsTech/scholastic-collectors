import logs
from scheduler import schedule_collectors
import logging

logging.getLogger("apscheduler").setLevel(logging.WARNING)

if __name__ == '__main__':
    schedule_collectors()
