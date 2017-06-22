import hashlib
from datetime import datetime
import pytz
from util.redis_client import RedisClient

utc = pytz.utc
fmt = '%Y-%m-%dT%H:%M:%S%z'
omp_time = datetime.strftime(utc.localize(datetime.utcnow()), fmt)

# message_writer = EsWriter(host='35.184.66.182')
message_writer = RedisClient(host='35.184.66.182', port=6379)


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
              platforms=[''], detailsURL='',severity=4):
    alert = {
        "storedTimestamp": omp_time,
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
        "isReset": False,
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
        "dateRaised": omp_time.split('T')[0],
        "monitoredCIName": "",
        "raisedLocalTimestamp": omp_time,
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
        "timestampUpdated": omp_time,
        "raisedTimestamp": omp_time,
        "dateHourEnded": None
    }

    alert['eventId'] = get_hash(event_hash_string(alert))
    alert['id'] = get_hash(event_id_string(alert))

    return alert


def send_event(triggerId, message='Test message', comments='Test Comments', title='Test title', description='',
               platforms=[''], detailsURL='',severity=4):
    alert_json = get_event(triggerId, message, comments, title, description, platforms, detailsURL,severity)
    message_writer.send_message(alert_json)
