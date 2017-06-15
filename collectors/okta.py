import json
from bs4 import BeautifulSoup
from utils import constants
from utils import templates
from selenium import webdriver
from db import ES_Reader as ES
import logging

logger = logging.getLogger(__name__)

driver = webdriver.PhantomJS()
driver.get(constants.URL_OKTA)
soup = BeautifulSoup(driver.page_source, 'html.parser')
# print soup.prettify()

HAPPY_STATE = 'all systems are operational'

html_tags = [
    ('h1', 'current-status__title current-status__title--good'),
]


def run():
    json_template = templates.get_json_template()
    json_template.update({
        'source': constants.SOURCE_OKTA,
        'sourceUrl': constants.URL_OKTA,
        'sourceStatus': constants.STATUS_GOOD,
    })

    try:
        service_status = None
        elements = []
        for tags in html_tags:
            elements = soup.find_all(tags[0], class_=tags[1])
            if elements:
                break

        if elements:
            service_status = elements[0].text.strip()

        # service_value = service_states_dict[service_name_and_status]

        json_template['services'].append({
            'name': 'okta',
            'value': service_status
        })

        if service_status.lower() != HAPPY_STATE:
            json_template['sourceStatus'] = constants.STATUS_CRITICAL

        # print json.dumps(json_template)
        ES.create_index_data(json_template)
    except Exception:
        logger.error('error parsing %s', constants.SOURCE_OKTA, exc_info=1)
        logger.error("-" * 100)
        logger.error(unicode(soup))
        logger.error("-" * 100)
        json_template['sourceStatus'] = constants.STATUS_CRITICAL
        ES.create_index_data(json_template)


if __name__ == '__main__':
    run()
