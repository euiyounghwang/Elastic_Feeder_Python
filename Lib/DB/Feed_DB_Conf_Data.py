
import os
import datetime
import configparser
import sys

import jaydebeapi as jdb_api
import pandas as pd
import pandas.io.sql as pd_sql
from pandas import DataFrame
import pympler.asizeof
import jpype

import ES_Feeder_Python.Config.getConfig as Config
import ES_Feeder_Python.Lib.Interface.Elastic_Bulk as Bulk
import ES_Feeder_Python.Lib.Logging.Logging as log
import ES_Feeder_Python.Lib.Util.Util as Utils
import re

# sys.path.append('/TOM/ES/')
# sys.path.append('/ES/')

from ES_Feeder_Python.Lib.DB.Feed_DB_Transaction import DB_Transaction_Cls
from ES_Feeder_Python.Lib.DB.Feed_DB_Conf import *

import ES_Feeder_Python.Lib.Feed_Text.Process_Queue as Queue_Transaction

ROWS_TOTAL_COUNT = 0
FILE_TOTAL_COUNT = 0


def Special_Charactor_Processing(sentence):
    """

    :param sentence:
    :return:
    """
    sentence = re.sub("None", "", sentence)
    sentence = re.sub("\r", "", sentence)
    sentence = re.sub("\n", "", sentence)

    sentence = re.sub("&amp;", "&", sentence)
    sentence = re.sub("&lt;", "<", sentence)
    sentence = re.sub("&gt;", ">", sentence)

    sentence = re.sub("<( )*style([^>])*?>", "<style>", sentence)
    sentence = re.sub("(<( )*(/)( )*?style( )*>)", "</style>", sentence)
    sentence = re.sub("<( )*STYLE([^>])*?>", "<style>", sentence)
    sentence = re.sub("(<( )*(/)( )*?STYLE( )*>)", "</style>", sentence)
    sentence = re.sub("(<style>)[\\s\\S]*?(</style>)", "", sentence)

    sentence = re.sub("<(/)?([a-zA-Z]*)(\\s[a-zA-Z]*=[^>]*)?(\\s)*(/)?>", "", sentence)
    sentence = re.sub("<(/)?([\\?])?([a-zA-Z]*(=)?(:)?[^ㄱ-ㅎㅏ-ㅣ가-힣][^>]*)?(\\s)*(/)?>", "", sentence)

    sentence = re.sub("<(/)?[bB][rR](\\s)*(/)?>", "", sentence)
    sentence = re.sub("[\\x00-\\x09\\x11\\x12\\x14-\\x1F\\x7F]", "", sentence)

    # sentence = re.sub(" ", "", sentence)
    sentence = re.sub("¡®", "", sentence)
    sentence = re.sub("¡¯", "", sentence)
    sentence = re.sub("\"", "", sentence)

    sentence = re.sub("&apos;", "'", sentence)
    sentence = re.sub("&nbsp;", " ", sentence)
    sentence = re.sub("&quot;", "", sentence)

    sentence = re.sub("&", "&amp;", sentence)
    sentence = re.sub("<", "&lt;", sentence)
    sentence = re.sub(">", "&gt;", sentence)
    sentence = re.sub("'", "&apos;", sentence)

    sentence = re.sub("\"", "&quot;", sentence)
    sentence = re.sub("(\r\n|\r|\n|\n\r)", "", sentence)

    # Control character(char code 12) Ascii CODE: ctrl + L(FORM FEED) 제거
    sentence = re.sub("[\\f]", "", sentence)

    # < / p > 태그
    sentence = re.sub("</[pP]>", "", sentence)

    # nbsp 제거
    sentence = sentence.replace("nbsp;", "")

    # \ 변환
    sentence = sentence.replace("\\\\", "&#92;");

    return sentence


def db_data_get_bulk_select_transaction(system_classfy, conn, params='', Is_Enable_Bulk_Options = False):
    """

    :param system_classfy:
    :param conn:
    :param params:
    :param Is_Enable_Bulk_Options:
    :return:
    """
    # conn = DB_Transaction_Cls(system_classfy).set_connection()
    try:
        print('\n\ndb_data_get_bulk_select_transaction')

        sql = get_bulk_sql_select_sql(system_classfy, Is_Enable_Bulk_Options)
        # print('sql ', sql)
        # params_colmun = ['LAW_ID', 'SUB_LAW_ID', 'INFRINGEMENT_ID', 'INFRINGEMENT_NAME']

        result_rows = []

        # df_all = pd_sql.read_sql_query(''.join(sql), conn, None)
        df_all = pd_sql.read_sql_query(''.join(sql), conn, params=params)
        # print('\n\n', df_all)
        # print('\n\n', df_all.keys(), len(df_all.keys()))

        # for column in df_all.keys():
        #     print(column)
        # import cx_Oracle
        # print('\n\n', df_all._get_values)

        # pip3 install pyhdb

        if df_all.shape[0] > 0:
            for loop in range(0, len(df_all._get_values)):
                results_dict = {}
                for column in df_all.keys():
                    # print(loop, column)
                    # print(loop, column, df_all.get(column)[loop])
                    # print(loop, df_all.get(column)[loop], df_all._get_values[loop][0])
                    results_dict[column] = str(df_all.get(column)[loop]).replace('None', '')\
                                                                        .replace('"','')\
                                                                        .replace('\r','')\
                                                                        .replace('\n','')


                if str(system_classfy).__eq__('ECM'):
                    Config.Gloal_Memory().set_global_key_memory(df_all.get('KEY')[loop], df_all.get('VERSION')[loop])

                result_rows.append(results_dict)
                loop += 1

        # df_temp = pd.DataFrame([df_all.get("DETECT_SENTENCE")[loop]],columns=["DETECT_SENTENCE"])
        # df=df.append(df_temp,ignore_index=True)
        # print(df)

    except Exception as ex:  # 에러 종류
         print('db_data_get_bulk_select_transaction >> ' + ex)

    # return []
    return result_rows


def get_Recordset_Feed(obj_feed, system_classfy, conn, ACTION_FLAG, params=[], idx=None, include_rownum_condition=True):
    """
    # DB SELECT ROWNUM
    new_params ['30', '20200902000000', 3601, 3700]
    :param obj_feed:
    :param system_classfy:
    :param conn:
    :param ACTION_FLAG:
    :param params:
    :param idx:
    :param include_rownum_condition:
    :return:
    """
    # elasticsearch 7.9 default '_doc'
    # obj_feed = Bulk.elasticsearch_interface(system_classfy, idx, None)
    # obj_feed.indics_set(idx, '_doc')
    # obj_feed = OBJ_CONFIG

    try:

        if not None in params:
            # print('get_Recordset_Feed.. <params> : ', params)
            log.info('get_Recordset_Feed.. ' + ','.join(params))

        paing_row_num = 100

        start_row_num = 1
        end_row_num = paing_row_num

        new_params = []

        for input in params:
            new_params.append(input)

        # QUERY ROWNUM++ 조건이 포함될경우
        if include_rownum_condition:
            new_params.append(start_row_num)
            new_params.append(end_row_num)

        # print('new_params', new_params)
        import ES_Feeder_Python.Lib.DB.Feed_DB_Transaction as Conn
        sql = db_config_setting().get_bulk_sql_select_sql(system_classfy)
        # print('sql ', sql)

        ######################################################
        ######################################################
        ######################################################
        # FILE DOC_ID 리스트 MAX수만큼 쿼리생성
        global FILE_TOTAL_COUNT
        if str(system_classfy).__contains__('FILE'):
            FILE_TOTAL_COUNT += len(new_params)
            print(Utils.bcolors().BOLD)
            print('## FILE DOC_ID LIST SEQUENCE : [' + str(FILE_TOTAL_COUNT) + ']')
            print(Utils.bcolors().ENDC)
            sql += " AND ("
            sql += "' OR ".join(("A.ECM_DOC_ID = '" + str(n) for n in new_params))
            sql += "')"
            # print('sql ', sql)
        ######################################################
        ######################################################
        ######################################################

        result_rows = []
        loop = 0
        max = 0.0

        global ROWS_TOTAL_COUNT

        while 1:
            print('\n' + Utils.bcolors().BOLD + Utils.bcolors().YELLOW + 'idx : ' + str(idx) + Utils.bcolors().ENDC)
            print(Utils.bcolors().BOLD + Utils.bcolors().YELLOW + 'new_params : ' + str(new_params) + Utils.bcolors().ENDC)
            print('\n')

            # df_all = pd_sql.read_sql_query(''.join(sql), conn, None)
            if str(system_classfy).__contains__('FILE') or str(system_classfy).__contains__('NO'):
                df_all = pd_sql.read_sql_query(''.join(sql), conn, params=None)
            else:
                df_all = pd_sql.read_sql_query(''.join(sql), conn, params=new_params)

            # pip3 install pyhdb
            if df_all.shape[0] > 0:
                for loop in range(0, len(df_all._get_values)):
                    results_dict = {}
                    for column in df_all.keys():
                        # print(loop, column, df_all.get(column)[loop])
                        # if str(column).__eq__('CONTENT'):
                        #     if (float)(max) <  (float)(str(df_all.get(column)[loop])):
                        #         max =  str(df_all.get(column)[loop])

                        results_dict[column] = Special_Charactor_Processing(str(df_all.get(column)[loop]))

                    print(loop, [results_dict])

                    # QUERY ROWNUM++ 조건이 포함될경우
                    # ARROWNUM, ROWNUM DELETE
                    if include_rownum_condition:
                        del results_dict['AROWNUM'], results_dict['ROWNUM']

                    # add meta
                    obj_feed.bulk_add_meta([results_dict], flag=ACTION_FLAG)

                    if obj_feed.get_lists_dict_length(obj_feed.StringBuffer) > obj_feed.memory_size:
                        print('\n')
                        log.info('StrigBuffer Send : ' + str(len(obj_feed.StringBuffer)) + ',\t' + str(obj_feed.get_lists_dict_length(obj_feed.StringBuffer)))
                        obj_feed.bulk_send(obj_feed.StringBuffer)
                        print('\n')
                        obj_feed.StringBuffer.clear()

                    loop += 1
                    ROWS_TOTAL_COUNT += 1

                new_params.clear()

                for input in params:
                    new_params.append(input)

                start_row_num += paing_row_num
                end_row_num += paing_row_num

                # QUERY ROWNUM++ 조건이 포함될경우
                if include_rownum_condition:
                    new_params.append(start_row_num)
                    new_params.append(end_row_num)

            else:
                log.info('No Recored...\n')
                break

            # QUERY ROWNUM++ 조건이 포함될경우 (ROWNUM 쿼리 미사용 시 한번 실행후 종료)
            if not include_rownum_condition:
                break

        if int(obj_feed.get_lists_dict_length(obj_feed.StringBuffer) > 0):
            print('\n')
            log.info('Remained StringBuffer Send : ' + str(len(obj_feed.StringBuffer)) + ',\t' + str(obj_feed.get_lists_dict_length(obj_feed.StringBuffer)))
            obj_feed.bulk_send(obj_feed.StringBuffer)
            print('\n')
            obj_feed.StringBuffer.clear()

        # print('max', max)

        # # Queue Creator
        # queue = ['F']
        # Queue_Transaction.Multiprocessing_Queue_Creator(queue)

    except Exception as ex:  # 에러 종류
         print('db_data_get_bulk_select_transaction >> ' + ex)

    # finally:
    #     obj_feed.elasticsearch_get_search()

    # return []
    return result_rows
