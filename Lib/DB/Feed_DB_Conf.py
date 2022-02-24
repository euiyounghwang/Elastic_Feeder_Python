import os
import datetime
import configparser
import sys
import yaml
import json

# sys.path.append('/TOM/ES/')
# sys.path.append('/ES/')

import ES_Feeder_Python.Config.getConfig as Config
import ES_Feeder_Python.Lib.Memory.Config_Initialize as Init_Memory

# config = configparser.ConfigParser()
# config.read('/ES/ES_Feeder_Python/Lib/DB/Feed_DB_Conf.ini')


class db_config_setting:

    def get_bulk_sql_select_sql(self, system_classfy):
        """

        :param system_classfy:
        :return:
        """

        query_memory = Init_Memory.Memory_Query_Object.get_global_query_xml_memory()

        if str(Init_Memory.Memory_Feed_Object.get_global_feed_xml_memory()['feed.bulk.mode']).__eq__('T'):
            query = str(query_memory['query_bulk'])
        else:
            query = str(query_memory['query_queue'])

        return query
