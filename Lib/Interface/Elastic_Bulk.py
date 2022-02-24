
# http://asuraiv.blogspot.com/2015/04/elasticsearch-versionconflictengineexce.html
# shell script

import elasticsearch
import pprint
import os
import json
import datetime
from elasticsearch import helpers
import sys

# sys.path.append(os.getcwd())
sys.path.append("/ES/")

import ES_Feeder_Python.Config.getConfig as Config
import ES_Feeder_Python.Lib.Interface.Query as Query
import ES_Feeder_Python.Lib.Interface.Elastic_Utils as ChkUtil
# from ES_Feeder_Python.Lib.Interface.Elastic_Utils import *
import ES_Feeder_Python.Lib.Util.Util as Util
import ES_Feeder_Python.Lib.Logging.Logging as log
from ES_Feeder_Python.Lib.Memory import Config_Initialize
import ES_Feeder_Python.Lib.Feed_Manage.Key_Manager as Manager

# noinspection PyMethodMayBeStatic,PyMethodParameters
class elasticsearch_interface:
    """
    https://programtalk.com/python-examples/elasticsearch.helpers.bulk/
    """

    def __init__(self, system_classfy,  index_name, doc_type='_doc', search_engine_ip=None):
        """

        :param system_classfy:
        :param index_name:
        :param doc_type:
        :param search_engine_ip:
        """
        # print('\n')
        # print('__init__(self)')


        if search_engine_ip is None:
            self.search_engine_list = str(Config_Initialize.Memory_Feed_Object.get_global_feed_xml_memory()["feed.search.engine.ip"]).split(",")
        else:
            self.search_engine_list = search_engine_ip

        self.elasticsearch_ip = self.search_engine_list

        self.system_classfy = system_classfy

        self.index_name = index_name
        self.doc_type = '_doc'

        self.StringBuffer = []
        self.StringKeyBuffer = {}
        self.memory_size = Config.CommonDefine().memory_size

        log.info('self.index_name >> ' + str(self.index_name))
        log.info('self.doctype >> ' + str(self.doc_type))
        log.info('self.elasticsearch_ip >> ' + str(self.elasticsearch_ip))

        self.header = {'Content-Type': 'application/json', 'Authorization': 'Basic ZWxhc3RpYzpnc2FhZG1pbg==', 'Connection': 'close'}
        self.es_client = None

        self.total, self.sucess, self.fail = 0, 0, 0


    def indics_set(self, indics_name, _type):
        self.index_name = indics_name
        self.doc_type = '_doc'


    def elastic_client_connect(self):
        self.es_client = elasticsearch.Elasticsearch(self.elasticsearch_ip,
                                                     # http_auth=('elastic', 'gsaadmin'),
                                                     headers=self.header,
                                                     timeout=10000
                                                     )

    def elastic_client_close(self):
        self.es_client.transport.connection_pool.close()


    def get_cat_aliase(self):
        """
        es.cat.indices(h='index', s='index').split()
        es.indices.get_alias("*")
        :return:
        """
        try:

            self.elastic_client_connect()
            # doc = self.es_client.cat.aliases(format(json))
            # doc = self.es_client.indices.get_alias("*")
            doc = self.es_client.cat.indices({"format": "json"})
            print('\n\n')
            print('## OUTPUT (get_cat_aliase) ##')
            print(json.dumps(doc, indent=2, ensure_ascii=False))

            # self.elasticsearch_get_search()

        except Exception as ex:  # 에러 종류
            print(ex)
            pass

        finally:
            self.elastic_client_close()


    def bulk_delete_bu_query(self):
        try:
            self.elastic_client_connect()

            doc = self.es_client.delete_by_query(
                               index = self.index_name,
                               doc_type=self.doc_type,
                               conflicts = 'proceed',
                               # refresh='wait_for',
                               wait_for_completion=True,
                               body = Query.elastic_query_match_all_search()
                            )
            print('\n\n')
            print('## OUTPUT (Delete By Query) ##')
            print(json.dumps(doc, indent = 2, ensure_ascii=False))

            # self.elasticsearch_get_search()

        except Exception as ex:  # 에러 종류
            print(ex)
            pass

        finally:
            self.self.elastic_client_close()



    def elasticsearch_get_search(self):

        try:
             self.self.elastic_client_connect()
             # doc = es_client.get(index = 'ict_ecm_grp_idx', doc_type = 'ict', id = 'doc0900bf4b9814ed4a')
             # doc = es_client.get(index = 'bank_version1', doc_type = 'account', id = 'new_id_1')

             # es_client.delete(index='bank_version1', doc_type='account', id='new_id_1')
             doc = self.es_client.search(index = self.index_name,
                              doc_type = self.doc_type,
                              body = Query.elastic_query_match_all_search()
                             )
             # print('\n\n')
             # pprint.pprint(doc)
             print('\n\n')
             print('## OUTPUT (Search) ##')
             print(json.dumps(doc, indent = 2, ensure_ascii=False))

        finally:
            self.elastic_client_close()


    def get_lists_dict_length(self, docs):
        total_size = 0
        for token in docs:
            total_size += len(str(token))

        return total_size


    def bulk_send(self, docs):
        """

        :param docs:
        :return:
        """
        # print('\nbulk_send1', docs)

        try:

            self.elastic_client_connect()

            success, failed, send_buffer_response = elasticsearch.helpers.custom_bulk(self.es_client, docs, raise_on_error=False, refresh=True)

            # print('\n\nbulk_send', success, failed)
            log.info('bulk_send >> success : ' + str(success) + ', failed : ' + str(failed))

            print('\n')
            log.info('*'*40)
            log.info('*' * 40)
            log.info('** Search Engine Send ...[' + str(self.elasticsearch_ip) + ']')
            log.info('*' * 40)
            log.info('*' * 40)

            feed_success_total_count, feed_fail_total_count, feed_sum_indexing_count = ChkUtil.elasticsearch_response(self.index_name,
                                                                                                                    self.StringKeyBuffer,
                                                                                                                    send_buffer_response)

            self.total += feed_sum_indexing_count
            self.sucess += feed_success_total_count
            self.fail += feed_fail_total_count

            print('\n\n')
            # print(Util.bcolors().BOLD + Util.bcolors().CYAN)
            print(Util.bcolors().BOLD + Util.bcolors().YELLOW)
            print('#' * 40)
            print('#' * 40)

            print('Bulk Indexing Search Engine >> {}'.format(self.elasticsearch_ip))
            print('Bulk Indexing SYSTEM_ID >> {}'.format(self.system_classfy))
            print('Bulk Indexing Target >> {}'.format(self.index_name))
            print('Bulk Indexing OneTime Size >> {}'.format(format(feed_sum_indexing_count, ",")))
            print('Bulk Indexing Success Size >> {}'.format(format(self.sucess, ",")))
            print('Bulk Indexing Faild Size >> {}'.format(format(self.fail, ",")))
            print('Bulk Indexing Total Size >> {}'.format(format(self.total, ",")))
            print('#' * 40)
            print('#' * 40)
            print(Util.bcolors().BOLD + Util.bcolors().ENDC)

        except Exception as ex:  # 에러 종류
            log.info(ex)
            # log.info(ex.args[0])
            # print('\nerror',json.dumps(ex.args[1], indent=2, ensure_ascii=False))
            # error_list = json.dumps(ex.args[1], indent=0, ensure_ascii=False)
            # Utils.elasticsearch_response(error_list)
            # results = json.dumps(ex.args[1], indent=2, ensure_ascii=False)
            pass

        finally:
            self.elastic_client_close()


    # noinspection PyShadowingNames
    # function 아래에서 메모리 처리 안함
    def bulk_add_meta(self, data, processing=None, flag='INSERT'):
        """
        # function 아래에서 메모리 처리 모두 함
           # '_source': {
                    #     'Law': '부당특약',
                    #     'CATEGORY': rows['category'],
                    #     'TRAIN_SOURCE': rows['train_source'],
                    #     'TRAIN_DETAIL_SOURCE': rows['train_detail_source'],
                    #     'FROM_SOURCE': rows['from_source'],
                    #     'FROM_SOURCE_URL': rows['from_source_url'],
                    #     'LABEL': str(rows['label']).upper(),
                    #     'SENTENCE': rows['sentence'],
                    #     'INPUTDATE': nowDatetime
        #   }
        :param data:
        :param processing:
        :param flag:
        :return:
        """
        now = datetime.datetime.now()
        nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')

        import binascii

        # for cnt in range(10):
        loop = 1
        for rows in data:
            # self.index_name = Manager.set_key_idx_name(self.index_name, rows)
            log.info('@@' + Manager.set_key_idx_name(self.index_name, rows) + '@@')
            # 첨부파일 동작 => 메시지큐 키 저장
            if str(Config_Initialize.Memory_Feed_Object.get_global_feed_xml_memory()['feed.file.use.yn']).__eq__('T'):
                if 'VERSION' in rows:
                    # ECM ATTACH
                    self.StringKeyBuffer[str(rows['KEY'])] = str(rows['VERSION'])
                    self.StringKeyBuffer['VERSION'] = str(rows['VERSION'])
                    self.StringKeyBuffer['OPERATION'] = 'doc'

            # ECM인 경우 하위폴더검색목적
            if 'ECM_FOLDER_ID_PATH' in rows:  rows['ECM_FOLDER_ID_PATH_ENCODE'] = str(binascii.hexlify(str(rows['ECM_FOLDER_ID_PATH']).encode('utf8'))).replace("b'",'').replace("'","").upper()

            # ECM인 경우 TARGET_URL 변경
            # if 'TARGET_URL' in rows:  rows['TARGET_URL'] = str(rows['TARGET_URL']).replace("&", "&amp;")

            if flag.__eq__('INSERT'):
                if 'KEY' in rows:
                    body = {
                        '_index': Manager.set_key_idx_name(self.index_name, rows),
                        # '_index': self.index_name,
                        '_type': self.doc_type,
                        '_id': Manager.set_key_value(str(rows['KEY'])),
                        '_source': dict(rows)
                    }

                elif 'DOCID' in rows:
                    body = {
                        # '_index': self.index_name,
                        '_index': Manager.set_key_idx_name(self.index_name, rows),
                        '_type': self.doc_type,
                        '_id': Manager.set_key_value(str(rows['DOCID'])),
                        '_source': dict(rows)
                     }

                elif 'EMPCD' in rows:
                    body = {
                        # '_index': self.index_name,
                        '_index': Manager.set_key_idx_name(self.index_name, rows),
                        '_type': self.doc_type,
                        '_id': Manager.set_key_value(str(rows['EMPCD'])),
                        '_source': dict(rows)
                    }
                elif 'ES_EMP_CD' in rows:
                    body = {
                        # '_index': self.index_name,
                        '_index': Manager.set_key_idx_name(self.index_name, rows),
                        '_type': self.doc_type,
                        '_id': Manager.set_key_value(str(rows['ES_EMP_CD'])),
                        '_source': dict(rows)
                    }
                else:
                    body = {
                        # '_index': self.index_name,
                        '_index': Manager.set_key_idx_name(self.index_name, rows),
                        '_type': self.doc_type,
                        '_source': dict(rows)
                    }

            elif flag.__eq__('DELETE'):
                 # print('@@@@@@@@DELETE')
                 body = {
                    '_op_type': 'delete',
                    # '_index': self.index_name,
                    '_index': Manager.set_key_idx_name(self.index_name, rows),
                    '_type': self.doc_type,
                    '_id': Manager.set_key_value(str(rows['KEY'])),
                    # '_id': 'new_id_' + str(loop)
                 }

            elif flag.__eq__('UPDATE_T') or flag.__eq__('UPDATE'):
                 body = {
                    '_op_type': 'update',
                    # '_index': self.index_name,
                    '_index': Manager.set_key_idx_name(self.index_name, rows),
                    '_type': self.doc_type,
                    '_id': Manager.set_key_value(str(rows['KEY'])),
                    # '_id': 'new_id_' + str(loop),
                    'doc': dict(rows),
                    'doc_as_upsert': True
                   }

            elif flag.__eq__('UPDATE_F'):
                body = {
                    '_op_type': 'update',
                    # '_index': self.index_name,
                    '_index': Manager.set_key_idx_name(self.index_name, rows),
                    '_type': self.doc_type,
                    '_id': Manager.set_key_value(str(rows['KEY'])),
                    # '_id': 'new_id_' + str(loop),
                    'doc': dict(rows),
                    'doc_as_upsert': False
                }

            self.StringBuffer.append(dict(body))

            current_memory = self.get_lists_dict_length(self.StringBuffer)
            print('\n' + Util.bcolors().BOLD + Util.bcolors().YELLOW + 'StringBuffer [Add Meta] ' + str(self.get_lists_dict_length(self.StringBuffer)) + 'Bytes /' + str(self.memory_size) + 'Bytes (Total Meta Buffer Ratio : ' +  str(round((float)(current_memory/self.memory_size),2)*100) + '%)' + Util.bcolors().ENDC)

            loop += 1
