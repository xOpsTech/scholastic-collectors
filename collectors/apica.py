import requests
from bs4 import BeautifulSoup
from utils import constants
from utils import templates
from db import ES_Reader as ES
import logging

logger = logging.getLogger(__name__)


# print soup.prettify()

def run():
    page = requests.get(constants.URL_APICA)
    soup = BeautifulSoup(page.content, 'html.parser')

    json_template = templates.get_json_template()
    json_template.update({
        'source': constants.SOURCE_APICA,
        'sourceUrl': constants.URL_APICA,
        'sourceStatus': constants.STATUS_GOOD,
    })
    try:
        service_status = constants.STATUS_GOOD
        status_dict = {
            'up': 0,
            'issue': 0,
            'down': 0
        }
        inner_containers = soup.find('div', class_='general_stat')
        service_circles = inner_containers.find_all('div', class_='service_circle')

        for circle in service_circles:
            service_n_status = circle.text.strip().split('\n')
            status_dict[service_n_status[1]] = int(service_n_status[0])
            # json_template['services'].append({
            #     'name': service_name,
            #     'value': service_value
            # })

        if status_dict.get('down') > 0:
            service_status = constants.STATUS_CRITICAL
        elif status_dict.get('issue') > 0:
            service_status = constants.STATUS_WARNING

        json_template['sourceStatus'] = service_status
        json_template['services'].append({
            'name': 'apica',
            'value': service_status
        })
        ES.create_index_data(json_template)
    except Exception:
        logger.error('error parsing %s', constants.SOURCE_APICA, exc_info=1)
        logger.error("-" * 100)
        logger.error(unicode(soup))
        logger.error("-" * 100)
        json_template['sourceStatus'] = constants.STATUS_CRITICAL
        ES.create_index_data(json_template)


if __name__ == '__main__':
    run()
