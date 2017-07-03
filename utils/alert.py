import hashlib
from datetime import datetime
import pytz
from utils.redis_client import RedisClient

utc = pytz.utc
fmt = '%Y-%m-%dT%H:%M:%S%z'
omp_time = datetime.strftime(utc.localize(datetime.utcnow()), fmt)

# message_writer = EsWriter(host='35.184.66.182')
message_writer = RedisClient(host='146.148.51.45', port=6379)


def event_hash_string(event_obj):
    hash_string = '%s%s%s' % (
        event_obj['producer'], event_obj['stateTriggerId'], event_obj['locationCode']
    )
    return hash_string


def event_id_string(event_obj):
    hash_string = '%s%s%s%s' % (
        event_obj['producer'], event_obj['stateTriggerId'], event_obj['locationCode'], event_obj['raisedTimestamp']
    )
    return hash_string


def get_hash(hash_string):
    return hashlib.md5(hash_string.encode('utf-8')).hexdigest()


def get_event(triggerId, message='Test message', comments='Test Comments', title='Test title', description='',
              platforms=[''], detailsURL='', severity=4, timestamp=omp_time, isReset=False):
    alert = {
        "storedTimestamp": timestamp,
        "assignedToName": "",
        "domain": "SUM",
        "extraData": {},
        "incidentNumber": "",
        "geolocLon": "",
        "sourceEventsCount": 1,
        "eventType": "Apica events",
        "platforms": platforms,
        "relatedDatesRaised": [],
        "detailsURL": detailsURL,
        "locationLabel": "",
        "message": message,
        "relatedStatesIds": [""],
        "isReset": isReset,
        "objectType": "alertState",
        "category": "Server",
        "monitoredCIID": "",
        "producer": "collector.apica.events",
        "objectId": "",
        "title": title,
        "trigger": "%s" % message,
        "comments": comments,
        "status": "new",
        "version": 1,
        "location": "",
        "KBArticle": "",
        "toolUUID": "",
        "testedLocation": "",
        "closedTimestamp": None,
        "relatedEventsIds": [""],
        "description": description,
        "workDuration": "",
        "locationCoordinates": [41.2619, 95.8608],
        "dateRaised": timestamp.split('T')[0],
        "monitoredCIName": "",
        "raisedLocalTimestamp": timestamp,
        "locationCode": "us-central1-f",
        "severity": severity,
        "count": "1",
        "stateTriggerId": "%s" % triggerId,
        "activeDuration": "",
        "monitoredCIClass": "",
        "assignedToId": "",
        "resetTimestamp": None,
        "geolocLat": "",
        "products": [""],
        "timestampUpdated": timestamp,
        "raisedTimestamp": timestamp,
        "dateHourEnded": None,
        "priority": "P3"
    }

    alert['eventId'] = get_hash(event_hash_string(alert))
    alert['id'] = get_hash(event_id_string(alert))

    return alert


def send_event(triggerId, message='Test message', comments='Test Comments', title='Test title', description='',
               platforms=[''], detailsURL='', severity=4, timestamp=omp_time):
    if severity in [3, 4]:
        is_reset = False
    else:
        is_reset = True

    alert_json = get_event(triggerId, message, comments, title, description, platforms, detailsURL, severity, timestamp,
                           is_reset)

    if severity == 3:
        alert_json['priority'] = 'P2'
    elif severity == 4:
        alert_json['priority'] = 'P1'

    message_writer.send_message(alert_json)
