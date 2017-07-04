from utils.apica import Client as ApicaClient
from utils.alert import send_event
from utils import constants
from db.sqlite_client import SqlLiteConnection
from db import ES_Reader as ES

apicaClient = ApicaClient()
sqlite_client = SqlLiteConnection()


def metrics():
    data = {"data": apicaClient.get_monitor_results_group_view()}
    ES.create_index_data(index='program_data', doc_type='program', body=data)


def events():
    event_list = apicaClient.get_monitors_by_severity('FWI')
    # print(event_list)
    for event in event_list:
        try:
            severity = constants.THRESHOLD_STATUS_OK
            if event['severity'] == 'F':
                severity = constants.THRESHOLD_STATUS_CRITICAL
            elif event['severity'] == 'W':
                severity = constants.THRESHOLD_STATUS_WARNING
            elif event['severity'] == 'I':
                severity = constants.THRESHOLD_STATUS_OK

            event_id = event['id']
            db_record = sqlite_client.get_event_by_id(event_id)

            if severity == constants.THRESHOLD_STATUS_OK:
                if db_record:
                    sqlite_client.delete_event(event_id)
                    check_id, location, severity, timestamp = db_record
                    # print check_id, location, severity, timestamp
                else:
                    continue

            else:
                location = event['location']
                timestamp = event['timestamp_utc']

                if db_record:
                    existing_timestamp = db_record[3]
                    if timestamp > existing_timestamp:
                        sqlite_client.update_event(event_id, severity, timestamp)
                    else:
                        print event_id, 'ignore duplicates'
                        continue
                else:
                    sqlite_client.insert_event(event_id, location, severity, timestamp)

            send_event(event_id, event['last_result_details']['message'], event['last_result_details']['message'],
                       event['url'] + ' : Issue in ' + location,
                       event['url'] + ' : Issue in ' + location, [""],
                       'https://wpm.apicasystem.com/Check/Details/' + str(event_id), severity, timestamp)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    print('started metrics processor ')
    # metrics()
    print('started event processor ')
    events()
    # t_metrics = threading.Thread(target=metrics)
    # e_metrics = threading.Thread(target=events)
    # t_metrics.daemon = True
    # e_metrics.daemon = True
    # t_metrics.start()
    # e_metrics.start()
