__author__ = 'Dinidu'

import logging
import sqlite3
import os

# DB = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'newrelic.db')
DB_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../scholastic_collector_db/'))
DB = os.path.join(DB_DIR, 'scholastic.db')

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)


class SqlLiteConnection(object):
    def __init__(self):

        self.logger = logging.getLogger(__name__)
        self.sql_events = 'create table if not exists events ' \
                          '(check_id VARCHAR PRIMARY KEY, location VARCHAR, severity VARCHAR, ' \
                          'timestamp VARCHAR)'
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute(self.sql_events)
        conn.close()

    def insert_event(self, check_id, location, severity, timestamp):

        conn, cursor = self.set_connection()
        with conn:
            try:
                cursor.execute(
                    'INSERT INTO events VALUES (?, ?, ?, ?)',
                    (check_id, location, severity, timestamp))

                self.logger.debug(
                    'process: insert event | parameters: {check_id: %s , location: %s , severity: %s, '
                    'timestamp: %s} | status: successful',
                    check_id, location, severity, timestamp)
            except Exception, e:
                self.logger.exception(e)
        conn.close()

    def update_event(self, check_id, severity, timestamp):
        conn, cursor = self.set_connection()
        with conn:
            try:
                cursor.execute('UPDATE events set severity=? , timestamp=? where check_id=?',
                               (severity, timestamp, check_id))
                self.logger.debug(
                    'process: update event | parameters: {severity: %s, timestamp: %s, check_id: %s} '
                    '| status: successful',
                    severity, timestamp, check_id)
            except Exception, e:
                self.logger.exception(e)
        conn.close()

    def delete_event(self, check_id):
        conn, cursor = self.set_connection()
        with conn:
            try:
                result = cursor.execute('DELETE FROM events WHERE check_id=?', (check_id,))
                self.logger.debug('process: delete event | parameters: {check_id: %s} | rows_deleted: %s | '
                                  'status: successful', check_id, result.rowcount)
            except Exception, e:
                self.logger.error('process: delete event | parameters: {check_id: %s} | status: unsuccessful', check_id)
                self.logger.exception(e)
        conn.close()

    def get_events(self):
        # with self.conn:
        result = None
        try:
            conn, cursor = self.set_connection()
            cursor.execute('SELECT * FROM events')
            self.logger.debug(
                'process: select events by event_type | parameters: {} | status: successful')
            result = cursor.fetchall()
        except Exception, e:
            self.logger.exception(e)
        finally:
            conn.close()

        return result

    def get_event_by_id(self, check_id):
        # with self.conn:
        result = None
        try:
            conn, cursor = self.set_connection()
            cursor.execute('SELECT * FROM events where check_id=?', (check_id,))
            self.logger.debug(
                'process: select event by check_id | parameters: {check_id: %s} | status: successful', check_id)
            result = cursor.fetchone()
        except Exception, e:
            self.logger.error(
                'process: select event by check_id | parameters: {check_id: %s} | status: unsuccessful', check_id)
            self.logger.exception(e)
        finally:
            conn.close()

        return result

    def is_exist_event(self, check_id):
        status = False

        try:
            # with self.conn:
            conn, cursor = self.set_connection()
            cursor.execute('SELECT check_id FROM events WHERE check_id=?', (check_id,))

            data = cursor.fetchone()
            self.logger.debug('process: does event exist | parameters: {check_id: %s} | status: successful', check_id)

            if data is not None:
                status = True

        except Exception, e:
            self.logger.error('process: does event exist | parameters: {check_id: %s} | status: unsuccessful', check_id)
            self.logger.exception(e)
        finally:
            conn.close()

        return status

    def set_connection(self):
        try:
            conn = sqlite3.connect(DB)
            cursor = conn.cursor()

            return conn, cursor

        except Exception as e:
            print e
