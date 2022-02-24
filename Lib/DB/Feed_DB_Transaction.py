import json

import jaydebeapi as jdb_api
import pandas as pd
import pandas.io.sql as pd_sql
from pandas import DataFrame

import ES_Feeder_Python.Config.getConfig as Config
import ES_Feeder_Python.Lib.Logging.Logging as log

# noinspection PyShadowingNames
import pympler.asizeof
import os
import jpype
import inspect
import ES_Feeder_Python.Lib.Memory.Config_Initialize as Init_Memory


# noinspection PyMethodMayBeStatic,PyShadowingNames
class DB_Transaction_Cls:

    def __init__(self):
       """
        jar='/ES/ES_UnFair_Detection/lib/Reference_Library/ojdbc6.jar'
        args = '-Djava.class.path=%s' % jar

        jvm_path = jpype.getDefaultJVMPath()
        jpype.startJVM(jvm_path, args)
       """
       self.conn = None

    def get_connection(self):
        return self.conn

    # noinspection PyAttributeOutsideInit
    def Set_DB_Connect(self):
        """

        :return:
        """
        Init_Memory.Memory_Feed_Object.get_global_feed_xml_memory()

        log.info('[' + inspect.currentframe().f_code.co_name + '] Set DB Connection Environment')

        self.conn = jdb_api.connect(Init_Memory.Memory_Feed_Object.get_global_feed_xml_memory()['feed.db.driver'],
                                    Init_Memory.Memory_Feed_Object.get_global_feed_xml_memory()['feed.db.url'],
                                    [Init_Memory.Memory_Feed_Object.get_global_feed_xml_memory()['feed.db.user'],
                                     Init_Memory.Memory_Feed_Object.get_global_feed_xml_memory()['feed.db.pwd']],
                                    Config.File().Server_JDBC_Driver)

        return self.conn

    def Set_DB_Disconnect(self, conn):
        """

        :param conn:
        :return:
        """
        if conn:
            if not conn._closed:
                conn.close()
                log.info('[' + inspect.currentframe().f_code.co_name + '] Set DB Disconnect...')




