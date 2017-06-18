import json
import requests
from bs4 import BeautifulSoup
from utils import constants
from utils import templates
from db import ES_Reader as ES
import logging

logger = logging.getLogger(__name__)

# print soup.prettify()

HAPPY_STATE = 'all systems operational'

service_states_dict = {
    'all systems operational': 'good',
    'major system outage': 'critical',
    'partial system outage': 'major',
    'minor system outage': 'minor'
}

html_tags = [
    ('span', 'status font-large'),
    ('a', 'actual-title with-ellipsis')
]


def run():
    page = requests.get(constants.URL_SUMOLOGIC)
    soup = BeautifulSoup(page.content, 'html.parser')

    json_template = templates.get_json_template()
    json_template.update({
        'source': constants.SOURCE_SUMOLOGIC,
        'sourceUrl': constants.URL_SUMOLOGIC,
        'sourceStatus': constants.STATUS_GOOD,
    })

    try:
        service_name_and_status = None
        elements = []
        for tags in html_tags:
            elements = soup.find_all(tags[0], class_=tags[1])
            if elements:
                break

        if elements:
            service_name_and_status = elements[0].text.strip().lower()

        # service_value = service_states_dict[service_name_and_status]

        json_template['services'].append({
            'name': 'sumologic',
            'value': service_name_and_status
        })

        if service_name_and_status.lower() != HAPPY_STATE:
            json_template['sourceStatus'] = constants.STATUS_CRITICAL

        # print json.dumps(json_template)
        ES.create_index_data(json_template)
    except Exception:
        logger.error('error parsing %s', constants.SOURCE_SUMOLOGIC, exc_info=1)
        logger.error("-" * 100)
        logger.error(unicode(soup))
        logger.error("-" * 100)
        json_template['sourceStatus'] = constants.STATUS_CRITICAL
        ES.create_index_data(json_template)


if __name__ == '__main__':
    run()
