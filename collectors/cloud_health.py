import json
import requests
from bs4 import BeautifulSoup
from utils import constants
from utils import templates
from db import ES_Reader as ES
import logging

logger = logging.getLogger(__name__)

page = requests.get(constants.URL_CLOUD_HEALTH)
soup = BeautifulSoup(page.content, 'html.parser')


def run():
    json_template = templates.get_json_template()
    json_template.update({
        'source': constants.SOURCE_CLOUD_HEALTH,
        'sourceUrl': constants.URL_CLOUD_HEALTH,
        'sourceStatus': constants.STATUS_GOOD,
    })
    try:
        inner_containers = soup.find_all('div', class_='component-inner-container')

        for container in inner_containers:
            service_name = container.find_all('span', class_='name')[0].text.strip()
            service_value = container.find_all('span', class_='component-status')[0].text.strip()
            json_template['services'].append({
                'name': service_name,
                'value': service_value
            })

        print json.dumps(json_template)
        ES.create_index_data(json_template)
    except Exception:
        logger.error('error parsing %s', constants.SOURCE_CLOUD_HEALTH, exc_info=1)
        logger.error("-" * 100)
        logger.error(unicode(soup))
        logger.error("-" * 100)
        json_template['sourceStatus'] = constants.STATUS_CRITICAL
        ES.create_index_data(json_template)


if __name__ == '__main__':
    run()
