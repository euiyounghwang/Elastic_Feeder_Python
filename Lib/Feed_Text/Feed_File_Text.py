
import os
import sys
import pandas as pd

# sys.path.append('/ES/')
sys.path.append('/TOM/ES/')

from  ES_Feeder_Python.Lib.Feed_Text.Socket.Socket_Client import *
import ES_Feeder_Python.Lib.Interface.Elastic_Bulk as Bulk
# from ES_Feeder_Python.Lib.Interface.Elastic_Bulk import *
import ES_Feeder_Python.Lib.Logging.Logging as log
from ES_Feeder_Python.Lib.Memory import Config_Initialize
import re


# /TOM/Python_Install/bin/python3 /TOM/ES/ES_Feeder_Python/Lib/Feed_Text/Feed_File_Text.py

# PATTERN = 'OBJECT_ID_'
PATTERN = '_elasticsearch_results_'
PATH = '/TOM/ES/ES_Feeder_Python/Lib/Feed_Text/Input/posco_ecm_grp1_idx/'
# PATH = '/ES/ES_Feeder_Python/Lib/Feed_Text/Input/OBJECT_ID_LIST'
# PATH = '/ES/ES_Feeder_Python/Lib/Feed_Text/Input/OBJECT_ID_LIST_bkp'


def file_open():
    """

    :return:
    """
    for filename in os.listdir(PATH):
        result_r = re.search(PATTERN, filename)
        if result_r:
            processing = []
            print('\n')
            log.info('@@@result_r@@@' + str(filename))
            object_id_list = []
            with open(PATH, 'r+', encoding='utf-8') as object_id_files:
                while True:
                    line = object_id_files.readline()
                    # if len(line) == 0:
                    if not line:
                        break

                    object_id_list.append(str(line).replace('\n', ''))

            print('\n\n')
            print('object_id_list ', object_id_list)

    return object_id_list



if __name__ == '__main__':

    # object_id_list = file_open()
    print('\n')

    # exit(1)
    # ******************************************************************************************************
    # ******************************************************************************************************
    # ******************************************************************************************************
    # Feed Initialize
    Config_Initialize.Memory_Common_Object.set_global_common_xml_memory('feed.file.limit.size', '104857600')
    # Feed Initialize
    Config_Initialize.Memory_Feed_Object.set_global_feed_xml_memory('feed.file.server.ip', '127.0.0.1')
    Config_Initialize.Memory_Feed_Object.set_global_feed_xml_memory('feed.file.server.port', 8192)
    Config_Initialize.Memory_Feed_Object.set_global_feed_xml_memory('feed.file.sever.id', 'accout')
    Config_Initialize.Memory_Feed_Object.set_global_feed_xml_memory('feed.file.sever.pw', 'passwd')
    Config_Initialize.Memory_Feed_Object.set_global_feed_xml_memory('feed.local.path', '/WAS/DATA/ES/DOWNLOAD_TEST/')
    Config_Initialize.Memory_Feed_Object.set_global_feed_xml_memory('feed.target.path', '/dec_files/')


    Config_Initialize.Memory_Feed_Object.set_global_feed_xml_memory('feed.file.use.yn', 'T')
    Config_Initialize.Memory_Feed_Object.set_global_feed_xml_memory('feed.remote_file.use.yn', 'F')
    # ******************************************************************************************************
    # ******************************************************************************************************
    # ******************************************************************************************************

    documents_read_count = 0.0
    MAX_CONTENT_LEN = 300
    loop = 1

    # SOCKET_SERVER_IP = '10.132.12.90'
    SOCKET_SERVER_IP = Config_Initialize.Memory_Feed_Object.get_global_feed_xml_memory()['feed.file.server.ip']
    SOCKET_SERVER_PORT = Config_Initialize.Memory_Feed_Object.get_global_feed_xml_memory()['feed.file.server.port']

    system_classfy = 'DOC'

    indices = ['TEST_idx', '_doc']

    SSH_OBJ = None

    obj_feed = Bulk.elasticsearch_interface(system_classfy=system_classfy,
                                            index_name=indices[0],
                                            doc_type=indices[1],
                                            search_engine_ip=['127.0.0.1:9200'])


    for filename in os.listdir(PATH):
        result_r = re.search(PATTERN, filename)
        if result_r:
            processing = []
            print('\n')
            log.info('@@@result_r@@@' + str(filename))

            content_key_object_df = pd.read_csv(PATH + str(filename), sep='\t', header=None, encoding='utf-8')
            # content_key_object_df = pd.read_csv(PATH, sep='\t', orient='index', columns=['sentence'], encoding='utf-8')
            content_key_object_df.dropna(how='any', inplace=True)
            # print(content_key_object_df.shape)
            # print(content_key_object_df.head(5))
            print('\n')
            # print('#1', content_key_object_df.values)
            # print(content_key_object_df[0][1])
            # print(content_key_object_df[1][1])
            print('\n')
            elements_df = [','.join(elements) for elements in content_key_object_df.values]
            # print('#2', elements_df)

            # 'doc0900bf4ba00caa95,0900bf4ba00caa95,2020-12-04 13:08:36', 'doc0900bf4ba00d16fe,0900bf4ba00d16fe,2020-12-04 17:22:26', 'doc0900bf4ba00a6ac3,0900bf4ba00a63ae,2020-12-02 13:05:48'
            client_socket = getSokcetTimeout(SOCKET_SERVER_IP, int(SOCKET_SERVER_PORT))
            for element in elements_df:
                element = str(element).split(',')
                print('\n')

                print(Utils.bcolors().BOLD)
                log.info('=' * 30)
                log.info("## [{:,}]".format(float(loop)))
                log.info('=' * 30)
                print(Utils.bcolors().ENDC)

                msg = 'ECM;' + element[1] + '\n'
                SSH_OBJ, full_contents = getSocketSend(client_socket, msg, default_view=False)

                if len(str(full_contents).strip()) > 0:
                    documents_read_count += 1
                    print('\n')
                    print('=' * 30)
                    print('=' * 30)
                    print("documents read.. : {:,}".format(float(documents_read_count)))
                    print('=' * 30)
                    print('=' * 30)

                    print(Utils.bcolors().BOLD)
                    if len(str(full_contents)) >= MAX_CONTENT_LEN:
                        log.info('Call Jar Text.. >> ' + str(full_contents)[:MAX_CONTENT_LEN])
                    else:
                        log.info('Call Jar Text.. >> ' + str(full_contents))
                        print(Utils.bcolors().ENDC)

                    # print(full_contents)
                    json_bulk = {
                        'KEY' : str(element[0]),
                        'INPUTDATE' : str(element[2]),
                        'CONTENT' : str(full_contents)
                    }

                    if len(str(element[2]).strip()) > 0:
                        obj_feed.bulk_add_meta([json_bulk], flag='UPDATE_F')
                        # obj_feed.bulk_add_meta([json_bulk], flag='UPDATE')

                if obj_feed.get_lists_dict_length(obj_feed.StringBuffer) > obj_feed.memory_size:
                    print('\n')
                    log.info('StrigBuffer Send : ' + str(len(obj_feed.StringBuffer)) + ',\t' + str(obj_feed.get_lists_dict_length(obj_feed.StringBuffer)))
                    obj_feed.bulk_send(obj_feed.StringBuffer)
                    print('\n')
                    obj_feed.StringBuffer.clear()

                loop += 1

            # socket client disconnect
            message = 'F'
            client_socket.sendall(message.encode('utf-8'))
            client_socket.close()

            # shell, sftp disconnect
            # SSH_OBJ.Set_SSH_Disconnection()

            if int(obj_feed.get_lists_dict_length(obj_feed.StringBuffer) > 0):
                print('\n')
                log.info('Remained StringBuffer Send : ' + str(len(obj_feed.StringBuffer)) + ',\t' + str(obj_feed.get_lists_dict_length(obj_feed.StringBuffer)))
                obj_feed.bulk_send(obj_feed.StringBuffer)
                print('\n')
                obj_feed.StringBuffer.clear()