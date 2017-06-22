import logging
from elasticsearch import Elasticsearch, NotFoundError

ELASTICSEARCH_HOST = 'localhost'
ELASTICSEARCH_PORT = 9200


class EsClient(object):
    def __init__(self, host=ELASTICSEARCH_HOST):
        self.es = Elasticsearch(host.split(','), timeout=20)
        self.logger = logging.getLogger(__name__)

    def read_index_data(self, index, doc_type, id):
        try:
            res = self.es.get(index=index, doc_type=doc_type, id=id)
            self.logger.info('action: query elasticsearch | index: %s | id: %s | status: successful', index, id)
            return res['_source']
        except NotFoundError as e:
            self.logger.error(
                'action: query elasticsearch | index: %s | id: %s | status: unsuccessful | reason: index not found',
                index, id)
            self.logger.error(e)
        except Exception as e:
            self.logger.error('action: query elasticsearch | index: %s | id: %s | status: unsuccessful', index, id)
            self.logger.exception(e)

    def create_index_data(self, index, doc_type, body):
        try:
            res = self.es.index(index=index, doc_type=doc_type, body=body)
            self.logger.info('action: write to elasticsearch | index: %s | id: %s | status: successful', index, id)
            return res['created']
        except Exception as e:
            self.logger.error('action: write to elasticsearch | index: %s | id: %s | status: unsuccessful', index, id)
            self.logger.exception(e)

    def search_index_data(self, index, query):
        try:
            res = self.es.search(index=index, body=query)
            self.logger.info('action: search elasticsearch | index: %s | query: %s | hits: %d | status: successful',
                             index, query, res['hits']['total'])
            return res['hits']['hits']
        except Exception as e:
            self.logger.error('action: search elasticsearch | index: %s | query: %s | status: unsuccessful', index,
                              query)
            self.logger.exception(e)

    def delete_index_data(self, index, doc_type, id):
        try:
            self.es.delete(index=index, doc_type=doc_type, id=id)
            self.logger.info('action: delete elasticsearch | index: %s | id: %s | status: successful', index, id)
        except Exception as e:
            self.logger.error('action: delete elasticsearch | index: %s | id: %s | status: unsuccessful', index, id)
            self.logger.exception(e)

    def update_index_data(self, index, doc_type, id, body):
        try:
            self.es.update(index=index, doc_type=doc_type, id=id, body=body)
            self.logger.info('action: update elasticsearch | index: %s | id: %s | status: successful', index, id)
            return True
        except Exception as e:
            self.logger.error('action: update elasticsearch | index: %s | id: %s | status: unsuccessful', index, id)
            self.logger.exception(e)

    def get_alert_by_event_id(self, index, doc_type, doc_id):
        return self.read_index_data(index=index, doc_type=doc_type, id=doc_id)

    def update_event(self, index, doc_type, body, alert_from_db):
        self.update_index_data(
            index=index, doc_type=doc_type, id=body['eventId'], body={
                "doc": {
                    "timestampUpdated": body['timestampUpdated'],
                    "severity": body['severity'],
                    "title": body['title'],
                    "trigger": body['trigger'],
                    "sourceEventsCount": int(alert_from_db.get('sourceEventsCount', 0)) + 1
                }
            })