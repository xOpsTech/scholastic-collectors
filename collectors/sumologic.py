import json
import requests
from bs4 import BeautifulSoup
from utils import constants
from utils import templates
from db import ES_Reader as ES

page = requests.get(constants.URL_SUMOLOGIC)
soup = BeautifulSoup(page.content, 'html.parser')
# print soup.prettify()

HAPPY_STATE = 'All Systems Operational'

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
    json_template = templates.get_json_template()
    json_template.update({
        'source': constants.SOURCE_SUMOLOGIC,
        'sourceUrl': constants.URL_SUMOLOGIC,
        'sourceStatus': constants.STATUS_GOOD,
    })

    service_name_and_status = None
    elements = []
    for tags in html_tags:
        elements = soup.find_all(tags[0], class_=tags[1])

    if elements:
        service_name_and_status = elements[0].text.strip().lower()

    # service_value = service_states_dict[service_name_and_status]

    json_template['services'].append({
        'name': 'sumologic',
        'value': service_name_and_status
    })

    print json.dumps(json_template)
    ES.create_index_data(json_template)


if __name__ == '__main__':
    run()
