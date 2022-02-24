
import os
from multiprocessing import Process, Lock, Queue, Manager, Pool
import ES_Feeder_Python.Lib.Util.Util as Utils
import ES_Feeder_Python.Lib.Logging.Logging as log
import ES_Feeder_Python.Lib.Memory.Config_Initialize as Init_Memory
from  ES_Feeder_Python.Lib.Feed_Text.Socket.Socket_Client import *
from datetime import datetime

write_queue = Queue()


def Multiprocessing_Queue_Creator(data):
    """
    Multi Process Queue
    :param data:
    :return:
    """
    log.info("Multiprocessing_Queue_Creator Start >> 프로세스 ID {0} (부모 프로세스 ID: {1})".format(os.getpid(), os.getppid()))
    for item in data:
        # log.info("Multiprocessing_Queue_Creator " + str(item))
        write_queue.put(item)


def Multiprocessing_Queue_Consumer():
    """

    :return:
    """
    start_time = datetime.now()
    from ES_Feeder_Python.Lib.Interface import Elastic_Bulk

    loaded_feed_config = Init_Memory.Memory_Feed_Object.get_global_feed_xml_memory()
    log.info("Multiprocessing_Queue_Consumer Start >> 프로세스 ID {0} : (부모 프로세스 ID: {1})".format(os.getpid(), os.getppid()))

    obj_feed = None
    SSH_OBJ = None
    client_socket = None
    idx_chk = ''
    full_text = ''
    documents_read_count = 0
    MAX_CONTENT_LEN = 300

    try:

        client_socket = getSokcetTimeout(loaded_feed_config['feed.file.server.ip'], int(loaded_feed_config['feed.file.server.port']))

        while True:
            queue_args = write_queue.get()

            print(Utils.bcolors().BOLD)
            log.info('Multiprocessing_Queue_Consumer >> ' + str(write_queue.qsize()) + ' >> ' + str(queue_args))
            # print('Multiprocessing_Queue_Consumer >> ' + str(write_queue.qsize()) + ' >> ' + str(queue_args))
            print(Utils.bcolors().ENDC)

            # StringKeyBuffer >>  {'doc0900bf4b9f0681dd': 'doc0900bf4b9f0681dd', 'VERSION': '0900bf4b9f0681dd', 'OPERATION': 'doc'}
            # => 최종 {'MESSAGE': 'pnr_ecm_grp_idx;doc0900bf4b9f0681dd,0900bf4b9f0681dd', 'SYS_ID': 'doc'}
            # if str(queue_args).__contains__('doc'):
            if 'SYS_ID' in dict(queue_args).keys():
                # if obj_feed is None: (idx 변할때 create object)
                if not str(idx_chk).__eq__(str(dict(queue_args)['MESSAGE']).split(';')[0]):
                    obj_feed = Elastic_Bulk.elasticsearch_interface(system_classfy='ECM',
                                                                index_name=str(dict(queue_args)['MESSAGE']).split(';')[0],
                                                                doc_type='_doc',
                                                                # search_engine_ip=['10.132.17.117:9201', '10.132.17.118:9201'])
                                                                search_engine_ip=None)

                    idx_chk = str(dict(queue_args)['MESSAGE']).split(';')[0]

                # ECM Socket Server
                if str(dict(queue_args)['SYS_ID']).__eq__('doc'):
                    # R_OBJECT_ID = str(queue_args).split(',')[1]

                    if client_socket is None:
                        log.info('@@@@@@@ client disconnected @@@@@@')

                    R_OBJECT_ID = str(dict(queue_args)['MESSAGE']).split(',')[1]
                    msg = 'ECM;' + R_OBJECT_ID + '\n'
                    SSH_OBJ, full_contents = getSocketSend(client_socket, msg, default_view=False)
                    documents_read_count += 1

                if len(str(full_contents).strip()) > 0:
                    print('\n')
                    print('=' * 30)
                    print('=' * 30)
                    print('documents read.. : ' + str(float(documents_read_count)))
                    print('=' * 30)
                    print('=' * 30)

                    print(Utils.bcolors().BOLD)
                    if len(str(full_contents)) >= MAX_CONTENT_LEN:
                        log.info('Call Jar Text.. >> ' + str(full_contents)[:MAX_CONTENT_LEN])
                    else:
                        log.info('Call Jar Text.. >> ' + str(full_contents))
                    print(Utils.bcolors().ENDC)

                # ******************************************************************
                # ******************************************************************
                # ******************************************************************
                # 첨부있을경우
                if len(str(full_contents).strip()) > 0:
                    # pnr_ecm_grp_idx;doc0900bf4b9f0446f8,0900bf4b9f0446f8
                    # CONTENT JSON
                    json_bulk = {
                        # 'KEY': str(queue_args).split(';')[1].split(',')[0],
                        'KEY': str(dict(queue_args)['MESSAGE']).split(';')[1].split(',')[0],
                        'CONTENT': str(full_contents)
                    }
                    # json_bulk['KEY'] = str(dict(queue_args)['MESSAGE']).split(';')[1].split(',')[0],
                    # json_bulk['CONTENT'] = str(full_contents)

                    obj_feed.bulk_add_meta([json_bulk], flag='UPDATE_F')
                    # obj_feed.bulk_add_meta([jso# n_bulk], flag='UPDATE')

                # ******************************************************************
                # ******************************************************************
                # ******************************************************************

                if obj_feed.get_lists_dict_length(obj_feed.StringBuffer) > obj_feed.memory_size:
                    print('\n')
                    log.info('StrigBuffer Send : ' + str(len(obj_feed.StringBuffer)) + ',\t' + str(obj_feed.get_lists_dict_length(obj_feed.StringBuffer)))
                    obj_feed.bulk_send(obj_feed.StringBuffer)
                    print('\n')
                    obj_feed.StringBuffer.clear()

            # if str(queue_args).__eq__(config.UserMemory().kill_message):
            if str(dict(queue_args)['MESSAGE']).__eq__("F"):
                if obj_feed:
                    if int(obj_feed.get_lists_dict_length(obj_feed.StringBuffer) > 0):
                        print('\n')
                        log.info('Remained StringBuffer Send : ' + str(len(obj_feed.StringBuffer)) + ',\t' + str(obj_feed.get_lists_dict_length(obj_feed.StringBuffer)))
                        obj_feed.bulk_send(obj_feed.StringBuffer)
                        print('\n')
                        obj_feed.StringBuffer.clear()

                    # socket client disconnect
                    message = 'F'
                    client_socket.sendall(message.encode('utf-8'))
                    client_socket.close()

                    # shell, sftp disconnect
                    if SSH_OBJ:
                        SSH_OBJ.Set_SSH_Disconnection()

                break


            # if str(queue_args).__eq__("F"):
            #     break

        end_time = datetime.now()

        print('\n')
        print('#' * 50)
        print('Queue_Consumer Start Time >> {}\nQueue_Consumer End Time >> {}'.format(start_time, end_time))
        print('Queue_Consumer RunningTime >> {}'.format(end_time - start_time))
        print('#' * 50)
        print('\n')

    except Exception as ex:  # 에러 종류
        print('Multiprocessing_Queue_Consumer >> ' + ex)