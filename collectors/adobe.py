import requests
from bs4 import BeautifulSoup
from utils import constants
from utils import templates
from selenium import webdriver
from db import ES_Reader as ES
import logging

logger = logging.getLogger(__name__)

driver = webdriver.PhantomJS()

# print soup.prettify()

HAPPY_STATE = 'functioning normally'


def run():
    driver.get(constants.URL_ADOBE)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    json_template = templates.get_json_template()
    json_template.update({
        'source': constants.SOURCE_ADOBE,
        'sourceUrl': constants.URL_ADOBE,
        'sourceStatus': constants.STATUS_GOOD,
    })
    try:
        service_status = constants.STATUS_GOOD

        cloud_name_list = soup.find_all('span', class_='cloud_name')
        status_list = soup.find_all('span', class_='status_text')

        for index, cloud_name in enumerate(cloud_name_list):
            service_name = cloud_name.text.strip()
            service_value = status_list[index].text.strip()
            json_template['services'].append({
                'name': service_name,
                'value': service_value
            })

            if service_value.lower() != HAPPY_STATE:
                service_status = constants.STATUS_CRITICAL

        json_template['sourceStatus'] = service_status

        # print json.dumps(json_template)
        ES.create_index_data(json_template)
    except Exception:
        logger.error('error parsing %s', constants.SOURCE_ADOBE, exc_info=1)
        logger.error("-" * 100)
        logger.error(unicode(soup))
        logger.error("-" * 100)
        json_template['sourceStatus'] = constants.STATUS_CRITICAL
        ES.create_index_data(json_template)


if __name__ == '__main__':
    run()
