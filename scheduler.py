from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
import collectors.cloud_health as cloud_health
import collectors.sumologic as sumologic
import collectors.netsuite as netsuite

JOB_MANAGER_POOL_SIZE = 5
SCHEDULER_INTERVAL = 10  # in seconds

executors = {
    'default': ThreadPoolExecutor(JOB_MANAGER_POOL_SIZE)
}
app_scheduler = BlockingScheduler(executors=executors)


def schedule_collectors():
    app_scheduler.add_job(cloud_health.run, 'interval', seconds=SCHEDULER_INTERVAL, id='apica_scheduler')
    app_scheduler.add_job(sumologic.run, 'interval', seconds=SCHEDULER_INTERVAL, id='sumologic_scheduler')
    app_scheduler.add_job(netsuite.run, 'interval', seconds=SCHEDULER_INTERVAL, id='netsuite_scheduler')

    app_scheduler.start()
