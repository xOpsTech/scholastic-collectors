from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
import collectors.cloud_health as cloud_health
import collectors.sumologic as sumologic
import collectors.netsuite as netsuite
import collectors.okta as okta
import collectors.aws as aws
import collectors.adobe as adobe

import collectors.apica_main as apicaMain

JOB_MANAGER_POOL_SIZE = 8
SCHEDULER_INTERVAL = 300  # in seconds

executors = {
    'default': ThreadPoolExecutor(JOB_MANAGER_POOL_SIZE)
}
app_scheduler = BlockingScheduler(executors=executors)


def schedule_collectors():
    pass
    app_scheduler.add_job(cloud_health.run, 'interval', seconds=SCHEDULER_INTERVAL, id='apica_scheduler')
    app_scheduler.add_job(sumologic.run, 'interval', seconds=SCHEDULER_INTERVAL, id='sumologic_scheduler')
    app_scheduler.add_job(netsuite.run, 'interval', seconds=SCHEDULER_INTERVAL, id='netsuite_scheduler')
    app_scheduler.add_job(okta.run, 'interval', seconds=SCHEDULER_INTERVAL, id='okta_scheduler')
    app_scheduler.add_job(aws.run, 'interval', seconds=SCHEDULER_INTERVAL, id='aws_scheduler')
    app_scheduler.add_job(adobe.run, 'interval', seconds=SCHEDULER_INTERVAL, id='adobe_scheduler')
    app_scheduler.add_job(apicaMain.metrics, 'interval', seconds=SCHEDULER_INTERVAL, id='apica_metrics_scheduler')
    app_scheduler.add_job(apicaMain.events, 'interval', seconds=SCHEDULER_INTERVAL, id='apica_events_scheduler')

    app_scheduler.start()
