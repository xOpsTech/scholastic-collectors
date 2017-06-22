import requests
import json
from multiprocessing.pool import ThreadPool as Pool
from threading import Thread
import threading
import json
from pprint import pprint

monitors_list = []
import time


class Client(object):
    __api_key = "046C9EA3-700B-44C1-ACC3-88FB44629491"
    __url = 'https://api-wpm.apicasystem.com/v3/'
    __uri = 'checks?enabled=enabled&auth_ticket='

    def __init__(self):
        __api_key = "046C9EA3-700B-44C1-ACC3-88FB44629491"
        __url = 'https://api-wpm.apicasystem.com/v3/'
        __uri = 'checks?enabled=enabled&auth_ticket='

    def __url_builder(self, uri='checks?enabled=enabled&auth_ticket='):

        build_url = self.__url + uri + self.__api_key
        return build_url

    def __remove_white_spaces_and_convert_to_lower_case(self, key):
        return key.lower().replace(" ", "")

    def __load_product_to_program_map(self):
        with open('../util/productTOprogramMap.json') as data_file:
            data = json.load(data_file)

        modified_data = {}
        for record in data:
            modified_data[self.__remove_white_spaces_and_convert_to_lower_case(record)] = data[record]
        return modified_data

    def __get_result(self, url):
        req = requests.request('GET', url)
        return req

    def get_monitors(self):
        results = self.__get_result(self.__url_builder())
        results_dict = json.loads(results.text)
        return results_dict

    def get_monitor_results_by_id(self, monitor_id, monitors_list=[]):

        results = self.__get_result(self.__url_builder('Checks/' + monitor_id + '?auth_ticket='))
        monitor = json.loads(results.text)
        monitors_list.append(monitor)
        # print (monitor)
        return monitor

    def get_monitors_by_severity(self, severity='F'):
        results = self.__get_result(self.__url_builder('checks?enabled=enabled&severity=' + severity + '&auth_ticket='))
        monitors = json.loads(results.text)
        return monitors

    def get_all_monitors_results(self, ddd=[]):
        pool_size = 10  # your "parallelness"
        pool = Pool(pool_size)
        monitors = self.get_monitors()
        for monitor in monitors:
            # print(monitor['name'])
            pool.apply_async(self.get_monitor_results_by_id, (str(monitor['id']), ddd,))
        pool.close()
        pool.join()
        return ddd

    def __construct_final_programe_map(self):
        final_list = []
        modified_monitor_results = []

        monitors_results = self.get_all_monitors_results()

        for monitor in monitors_results:
            # print(monitor)
            modified_monitor = {}
            map = self.__load_product_to_program_map()
            try:
                modified_monitor['name'] = monitor['name']
                modified_monitor['id'] = monitor['id']
                modified_monitor['severity'] = monitor['severity']
            except:
                print(monitor)
                continue

            try:
                modified_monitor['program'] = map[self.__remove_white_spaces_and_convert_to_lower_case(monitor['name'])]
            except:
                modified_monitor['program'] = 'Other'

            modified_monitor_results.append(modified_monitor)

        return modified_monitor_results

    def get_monitor_results_group_view(self):

        monitor_results_group_view_list = []

        modified_monitor_results = self.__construct_final_programe_map()

        group_dict = {}
        programs = []

        for monitor in modified_monitor_results:


            if monitor['program'] not in programs:
                monitor['F_count'] = 0
                monitor['I_count'] = 0
                monitor['W_count'] = 0

                monitor['F_names'] = []
                monitor['I_names'] = []
                monitor['W_names'] = []




                if monitor['severity'] == 'F':
                    monitor['F_count'] = 1
                    monitor['F_names'].append(monitor['name'])

                elif monitor['severity'] == 'I':
                    monitor['I_count'] = 1
                    monitor['I_names'].append(monitor['name'])

                elif monitor['severity'] == 'W':
                    monitor['W_count'] = 1
                    monitor['W_names'].append(monitor['name'])

                monitor.pop('severity', None)
                monitor.pop('name', None)
                monitor.pop('id', None)

                programs.append(monitor['program'])
                group_dict[monitor['program']] = monitor
                monitor_results_group_view_list.append(monitor)
            else:

                for program_dict in monitor_results_group_view_list:
                    try:
                        if monitor['program'] == program_dict['program']:

                            temp = program_dict

                            if monitor['severity'] == 'F':
                                temp['F_count'] = temp['F_count'] + 1
                                temp['F_names'].append(monitor['name'])

                            elif monitor['severity'] == 'I':
                                temp['I_count'] = temp['I_count'] + 1
                                temp['I_names'].append(monitor['name'])

                            elif monitor['severity'] == 'W':
                                temp['W_count'] = temp['W_count'] + 1
                                temp['W_names'].append(monitor['name'])

                            monitor_results_group_view_list.remove(program_dict)
                            monitor_results_group_view_list.append(temp)
                    except:
                        print('--------------------')
        for monitor_status in monitor_results_group_view_list:

            if monitor_status['F_count'] > 0:
                monitor_status['status'] = 'red'
            elif monitor_status['F_count'] == 0 and monitor_status['W_count'] > 0 :
                monitor_status['status'] = 'amber'
            elif monitor_status['F_count'] == 0 and monitor_status['W_count'] == 0 and monitor_status['I_count'] > 0:
                monitor_status['status'] = 'green'
            else :
                monitor_status['W_count'] = 'gray'

        return monitor_results_group_view_list


# dd = Client()
# ddd = []
# # ff= dd.get_all_monitors_results()
# # ff= dd.construct_final_programe_map()
# ff = dd.get_monitors_by_severity()
# # ff = dd.get_monitor_results_group_view()
# print(ff)
# # dict = dd.get_all_monitors_results(ddd)
# # dict = dd.get_monitors_by_severity()
# # dict = dd.get_monitor_results_by_id('125124')
# # dict = dd.get_monitors()
# # print(dict)
# # for i in dict:
# #     print(i['name'])
