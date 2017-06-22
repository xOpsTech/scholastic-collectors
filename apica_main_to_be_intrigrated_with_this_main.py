from util.esClient import EsClient
from util.apica import Client as ApicaClient
from util.alert import send_event
import json
import threading

es_client = EsClient(host='35.184.66.182')
apicaClient = ApicaClient()


def metrics():
    data = {"data": apicaClient.get_monitor_results_group_view()}
    es_client.create_index_data(index='program_data', doc_type='program', body=json.dumps(data))


def events():
    event_list = apicaClient.get_monitors_by_severity('FW')
    print(event_list)
    for event in event_list:
        try:

            severity = 0
            if event['severity'] == 'F':
                severity = 3
            elif event['severity'] == 'W':
                severity = 3
            elif event['severity'] == 'I':
                severity = 0
            else:
                severity = 0
            send_event(event['id'], event['last_result_details']['message'], event['last_result_details']['message'],
                       event['url'] + ' : Issue in ' + event['location'],
                       event['url'] + ' : Issue in ' + event['location'], [""],
                       'https://wpm.apicasystem.com/Check/Details/' + str(event['id']), severity)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    print('started metrics processor ')
    metrics()
    print('started event processor ')
    # events()
    # t_metrics = threading.Thread(target=metrics)
    # e_metrics = threading.Thread(target=events)
    # t_metrics.daemon = True
    # e_metrics.daemon = True
    # t_metrics.start()
    # e_metrics.start()
