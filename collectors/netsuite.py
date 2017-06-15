# https://stackoverflow.com/questions/2148493/scrape-html-generated-by-javascript-with-python
# http://phantomjs.org/download.html
# https://stackoverflow.com/questions/8778513/how-can-i-setup-run-phantomjs-on-ubuntu

import json
from bs4 import BeautifulSoup
from utils import constants
from utils import templates
from selenium import webdriver
from db import ES_Reader as ES
import logging

logger = logging.getLogger(__name__)

driver = webdriver.PhantomJS()
driver.get(constants.URL_NETSUITE)
soup = BeautifulSoup(driver.page_source, 'html.parser')
# print soup.prettify()

HAPPY_STATE = 'all systems are operational'

status_icon_dict = {
    'icon-icon_messaging_available': constants.STATUS_GOOD,
    'icon-icon_messaging_disruption': constants.STATUS_CRITICAL
}


def run():
    json_template = templates.get_json_template()
    json_template.update({
        'source': constants.SOURCE_NETSUITE,
        'sourceUrl': constants.URL_NETSUITE,
        'sourceStatus': constants.STATUS_GOOD,
    })

    try:
        service_status = constants.STATUS_GOOD

        table = soup.find('table', attrs={'id': 'weekly-status'})
        table_body = table.find('tbody')

        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            service_name = cols[0].text.strip()
            service_value_icon = cols[1].find('svg').get('class')[1]
            service_value = status_icon_dict[service_value_icon]

            if service_value == constants.STATUS_CRITICAL:
                service_status = service_value

            json_template['services'].append({
                'name': service_name,
                'value': service_value
            })

        json_template['sourceStatus'] = service_status

        # print json.dumps(json_template)
        ES.create_index_data(json_template)
    except Exception:
        logger.error('error parsing %s', constants.SOURCE_NETSUITE, exc_info=1)
        logger.error("-" * 100)
        logger.error(unicode(soup))
        logger.error("-" * 100)
        json_template['sourceStatus'] = constants.STATUS_CRITICAL
        ES.create_index_data(json_template)


if __name__ == '__main__':
    run()
