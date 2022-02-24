# -*- coding: utf-8 -*-
import logging
import base64
from importlib import reload
# from matplotlib import font_manager, rc
import jaydebeapi as jdb_api
from multiprocessing import Process, Lock, Queue, Manager

################################################
################################################
################################################
# 프로젝트에서 공통으로 사용하는 변수 선언
################################################
################################################
################################################
class CommonDefine:
    # ------------------------------
    # -- Server, Local 실행 여부
    # ------------------------------
    # isStartWhichInfra = "T"
    isStartWhichInfra = "F"

    # ------------------------------
    # -- Multiple Processing 여부
    # ------------------------------
    isMultipleProcessing = True
    # isMultipleProcessing = False

    # ------------------------------
    # -- Logging
    # ------------------------------
    isSetLogging = 'T'

    # ------------------------------
    # -- 실제 컨텐츠 파일패턴(READ)
    # ------------------------------
    global_indics_type = ['bank_version1', 'account']

    # ------------------------------
    # -- 색인 메모리 버퍼 사이즈
    # ------------------------------
    # memory_size = 524288
    memory_size = 1048576

    # Path = '/ES/ES_Bulk_Incre_Project/Input/Law/'
    # PATTERN = 'Initial_Training'


    # PROD_BULK >> 30 >> ECM >> posco_ecm_grp1_idx
    Path = '/home/PROD_BULK/TEST_IDX/'
    PATTERN = '_elasticsearch_'

    # ------------------------------
    # -- 전체 반영 (DB -> SEARCH)
    # ------------------------------
    index_total_count = 0

    def set_index_total_count(self):
        self.index_total_count += 1

    def get_index_total_count(self):
        return self.index_total_count


class Gloal_Memory:

    def __init__(self):
        self.key_management = {}


    def get_global_key_memory(self):
        return self.common_xm_dic

    def set_global_key_memory(self, key, value):
        if key not in self.key_management.keys():
            self.key_management[key] = value
        else:
            self.key_management[key] = value


class APP_Memory:

    def __init__(self):

        # global common_xm_dic

        self.common_xm_dic = {}
        self.feed_xml_dic = {}
        self.feed_query_dic = {}


    def set_all_memory_clear(self):
        self.common_xm_dic.clear()
        self.feed_xml_dic.clear()
        self.feed_query_dic.clear()


    def get_global_common_xml_memory(self):
        return self.common_xm_dic

    def set_global_common_xml_memory(self,  key, value):
        if key not in self.common_xm_dic.keys():
            self.common_xm_dic[key] = value
        else:
            self.common_xm_dic[key] = value

    def get_global_feed_xml_memory(self):
        return self.feed_xml_dic

    def set_global_feed_xml_memory(self, key, value):
        if key not in self.feed_xml_dic.keys():
            self.feed_xml_dic[key] = value
        else:
            self.feed_xml_dic[key] = value

    def get_global_query_xml_memory(self):
        return self.feed_query_dic

    def set_global_query_xml_memory(self, key, value):
        if key not in self.feed_xml_dic.keys():
            self.feed_query_dic[key] = value
        else:
            self.feed_query_dic[key] = value




class File:

    def __init__(self):

        if str(CommonDefine().isStartWhichInfra).__eq__('T'):
            self.root_path = '/TOM/ES'
            self.Server_JDBC_Driver =  self.get_Root_Directory() + '/ES_Feeder_Python/Lib/DB/ojdbc6.jar'
            self.Server_Logging_Path = self.get_Root_Directory() + '/ES_Feeder_Python/'

        else:
            self.root_path = '/ES'
            self.Server_JDBC_Driver = self.get_Root_Directory() + '/ES_Feeder_Python/Lib/DB/ojdbc6.jar'
            self.Local_Logging_Path = self.get_Root_Directory() + '/ES_Feeder_Python/'


    def get_Root_Directory(self):
        return self.root_path

    def getOutputFilePath(self):
        if CommonDefine().isStartWhichInfra == "T":
            return self.Server_Logging_Path
        else:
            return self.Local_Logging_Path

    # Server_JDBC_Driver = '/TOM/ES/ES_Bulk_Incre_Project/Lib/DB/ojdbc6.jar'
    # Server_JDBC_Driver = '/ES/ES_Bulk_Incre_Project/Lib/DB/ojdbc6.jar'


