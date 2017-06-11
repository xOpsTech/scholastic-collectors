import json
import requests
from bs4 import BeautifulSoup
from utils import constants
from utils import templates
from db import ES_Reader as ES

page = requests.get(constants.URL_CLOUD_HEALTH)
soup = BeautifulSoup(page.content, 'html.parser')


def run():
    json_template = templates.get_json_template()

    inner_containers = soup.find_all('div', class_='component-inner-container')
    json_template.update({
        'source': constants.SOURCE_CLOUD_HEALTH,
        'sourceUrl': constants.URL_CLOUD_HEALTH,
        'sourceStatus': constants.STATUS_GOOD,
    })

    for container in inner_containers:
        service_name = container.find_all('span', class_='name')[0].text.strip()
        service_value = container.find_all('span', class_='component-status')[0].text.strip()
        json_template['services'].append({
            'name': service_name,
            'value': service_value
        })

    print json.dumps(json_template)
    ES.create_index_data(json_template)


if __name__ == '__main__':
    run()
