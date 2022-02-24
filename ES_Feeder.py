# -*- coding: utf-8 -*-

import sys
import os
import schedule
from multiprocessing import Process, Lock, Queue, Manager, Pool
import jpype

# sys.path.append(os.getcwd())
# sys.path.append("/ES/")
sys.path.append("/TOM/ES/")
# sys.path.append("D://POSCOICT/Project/Source/Python/")

# /TOM/Python_Install/bin/python3.5 /TOM/ES/ES_Bulk_Incre_Project/ES_Crawled_DB_Bulk.py
# /TOM/Python_Install/bin/python3.5 /TOM/ES/ES_Feeder_Python/ES_Feeder.py G_ECM

import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta

import time
# import datetime
import ES_Feeder_Python.Lib.Logging.Logging as log
import ES_Feeder_Python.Config.getConfig as Config
import ES_Feeder_Python.Lib.Interface.Directory_Utils as Directory_Util
import ES_Feeder_Python.Lib.Util.Util as Utils

import ES_Feeder_Python.Lib.Memory.Config_Initialize as Init_Memory
import ES_Feeder_Python.Lib.DB.Feed_Query_Manage as Manage_QueryParam
import ES_Feeder_Python.Lib.Feed_Manage.Manager as Feed_Manager
import ES_Feeder_Python.Lib.Feed_Text.Process_Queue as Queue_Transaction
import ES_Feeder_Python.Lib.Interface.Elastic_Bulk as Bulk
import ES_Feeder_Python.Lib.File_IO.File_Transaction as File_Call

# ACTION_FLAG = 'INSERT'
# ACTION_FLAG = 'UPDATE'
ACTION_FLAG = 'UPDATE_T'
# ACTION_FLAG = 'UPDATE_F'
# ACTION_FLAG = 'DELETE'


loaded_feed_config = None

def Feed_Meta_Job(isTimer, SYSTEM_ID, IS_QUERY_WITH_ROWNUM):
    """
    import ES_Bulk_Incre_Project.Lib.Interface.Elastic_Bulk as Bulk
    indics_type = ['bank_version1', 'account']
    # delte_data = [{'KEY': 'piCfEXQBXUqa8NCrfn_u'}, {'KEY': 'xSBLFXQB2uAYsLae85XL'}, {'KEY': '8CCeEXQBXUqa8NCre34A'}]
    Bulk.elasticsearch_interface(indics_type[0], indics_type[1]).bulk_add_buffer(result_sets, flag='DELETE')
    log.info('result_sets ' + str(len(result_sets)))

    # START_DATE = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d") + time.strftime('%H%M%S')
    # END_DATE = (datetime.date.today() - datetime.timedelta(days=0)).strftime("%Y%m%d") + time.strftime('%H%M%S')

    :param isTimer:
    :param SYSTEM_ID:
    :param IS_QUERY_WITH_ROWNUM:
    :return:
    """
    start_time = datetime.now()

    log.info("#####################################")
    # log.info('StartTime ' + str(start_time))
    print('\n\nPython Based Feeder Starting...')
    print('\n\n')

    import ES_Feeder_Python.Lib.DB.Feed_DB_Conf_Data as get_rows
    import ES_Feeder_Python.Lib.DB.Feed_DB_Transaction as Conn

    try:

        # jar = Config.File().get_Root_Directory() + '/ES_Bulk_Incre_Project/Lib/DB/ojdbc6.jar'
        jar = Config.File().Server_JDBC_Driver
        args = '-Djava.class.path=%s' % jar

        jvm_path = jpype.getDefaultJVMPath()
        # jpype.startJVM(jvm_path, args)
        # Init_Memory.init_jvm(jvm_path, args)
        Init_Memory.init_jvm_environment(jvm_path, args)

        # Get common. feeed. query xml loading..
        # Init_Memory.Initialize_Config_Loading(SYSTEM_ID)

        # Feed Memory Config
        loaded_feed_config = Init_Memory.Memory_Feed_Object.get_global_feed_xml_memory()

        conn = Conn.DB_Transaction_Cls().Set_DB_Connect()

        # START_DATE = '20200909000000'
        # START_DATE = '20200801000000'
        # START_DATE = (datetime.date.today() - datetime.timedelta(days=2)).strftime("%Y%m%d") + '000000'

        OBJ_CONFIG = Config.CommonDefine()
        OBJ_Memory = Config.APP_Memory()

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # PARAMS Settings
        # ip = Feed_Manager.get_manipulate_idx(SYSTEM_ID, loaded_feed_config["feed.search.engine.ip"])
        ip = loaded_feed_config["feed.search.engine.ip"]
        idx_dic = Feed_Manager.get_manipulate_idx(SYSTEM_ID, loaded_feed_config["feed.search.engine.idx"])
        START_DATE = loaded_feed_config["feed.start.date"]
        END_DATE = loaded_feed_config["feed.end.date"]
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # Initialize
        OBJ_Memory.set_all_memory_clear()
        # idx Initialze_delete_all_idx
        Feed_Manager.INIT_DELETE_IDX(SYSTEM_ID, idx_dic)
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


        # Conn.DB_Transaction_Cls().Set_DB_Disconnect(conn)
        # exit()
        # elasticsearch 7.9 default '_doc'
        # obj_feed = Bulk.elasticsearch_interface(SYSTEM_ID)
        if not str(START_DATE).__eq__('None') and not str(END_DATE).__eq__('None'):
            print('\nExist Date ..')
            start = datetime.strptime(START_DATE, '%Y%m').date()
            end = datetime.strptime(END_DATE, '%Y%m').date()

            # ACTION_FLAG[1] 'INSERT' or 'DELETE'
            # <feed.compcode.info>30,01</feed.compcode.info>
            for COMPANY_CODE in str(loaded_feed_config["feed.compcode.info"]).split(","):

                cur_date = start
                # elasticsearch 7.9 default '_doc'
                OBJ_CONFIG = Bulk.elasticsearch_interface(SYSTEM_ID, idx_dic[COMPANY_CODE], search_engine_ip=None)

                while cur_date <= end:
                    # print(str(cur_date)[:4] + str(cur_date)[5:7])
                    YYYYMM_DATE = str(cur_date)[:4] + str(cur_date)[5:7]

                    YYYYMM_CURRENT_START_DATE = YYYYMM_DATE + '01' + '000000'
                    YYYYMM_CURRENT_END_DATE = YYYYMM_DATE + str(calendar.monthrange(int(str(YYYYMM_DATE)[:4]), int(str(YYYYMM_DATE)[4:6]))[1]) + '235959'
                    # print('END_DATE' + '\t' + END_DATE)
                    # print(YYYYMM_CURRENT_START_DATE + '\t' + YYYYMM_CURRENT_END_DATE)
                    # YYYYMM_CURRENT_START_DATE = 20191201000000  20191201235959
                    # YYYYMM_CURRENT_END_DATE = 20191202000000  20191202235959
                    # for day in range(1, int(calendar.monthrange(int(str(YYYYMM_DATE)[:4]), int(str(YYYYMM_DATE)[4:6]))[1]) + 1):
                    #     YYYYMM_CURRENT_START_DATE = YYYYMM_DATE + str(day).zfill(2) + '000000'
                    #     YYYYMM_CURRENT_END_DATE = YYYYMM_DATE + str(day).zfill(2) + '235959'
                        # print(YYYYMM_CURRENT_START_DATE + '\t' + YYYYMM_CURRENT_END_DATE)

                        # YYYYMM_CURRENT_START_DATE = 20191201000000  20191201005959
                        # YYYYMM_CURRENT_END_DATE = 20191201010000  20191201015959
                        # for hour in range(0, 24):
                        #     YYYYMM_CURRENT_START_DATE = YYYYMM_CURRENT_START_DATE[:8] + str(hour).zfill(2) + '0000'
                        #     YYYYMM_CURRENT_END_DATE = YYYYMM_CURRENT_END_DATE[:8] + str(hour).zfill(2) + '5959'
                        #     print(YYYYMM_CURRENT_START_DATE + '\t' + YYYYMM_CURRENT_END_DATE)

                    result_sets = get_rows.get_Recordset_Feed(OBJ_CONFIG,
                                                                  SYSTEM_ID,
                                                                  conn,
                                                                  ACTION_FLAG,
                                                                  params=Manage_QueryParam.get_system_query_param(SYSTEM_ID, COMPANY_CODE, START_DATE=YYYYMM_CURRENT_START_DATE, END_DATE=YYYYMM_CURRENT_END_DATE),
                                                                  idx=idx_dic[COMPANY_CODE],
                                                                  include_rownum_condition=IS_QUERY_WITH_ROWNUM)
                    cur_date += relativedelta(months=1)

        else:
            print('\n\nNo Date Options..')

            if str(SYSTEM_ID).__contains__('FILE'):
                is_File_ECM_DOC = True
            else:
                is_File_ECM_DOC = False

            # FILE DOC_ID 리스트에서 처리하는 로직 필요
            # FILE에서 읽어서 DB DOC_ID 건건이 조회해서 첨부처리
            if is_File_ECM_DOC:
                COMPANY_CODE = ''.join(str(loaded_feed_config["feed.compcode.info"]).split(","))
                # elasticsearch 7.9 default '_doc'
                OBJ_CONFIG = Bulk.elasticsearch_interface(SYSTEM_ID, idx_dic[COMPANY_CODE], search_engine_ip=None)

                # Query In 절
                Max_In_Size = 100

                # for DOC_ID_GROUP in File_Call.file_doc_id_list():
                for loop in range(0, int(len(File_Call.file_doc_id_list()) / Max_In_Size) + 1):
                    # print('\n', DOC_ID)
                    # DOC_ID_GROUP = "','".join(File_Call.file_doc_id_list()[loop * Max_In_Size:(loop * Max_In_Size) + Max_In_Size])
                    # DOC_ID_GROUP = ("'" + DOC_ID_GROUP + "'")
                    # DOC_ID_GROUP = ('doc0900bf4ba00a6ac2','doc0900bf4ba00eb3e0')
                    DOC_ID_GROUP = File_Call.file_doc_id_list()[loop * Max_In_Size:(loop * Max_In_Size) + Max_In_Size]
                    if DOC_ID_GROUP:
                        result_sets = \
                            get_rows.get_Recordset_Feed(OBJ_CONFIG,
                                                        SYSTEM_ID,
                                                        conn,
                                                        ACTION_FLAG,
                                                        params=Manage_QueryParam.get_system_query_param(SYSTEM_ID,
                                                                                                        COMPANY_CODE,
                                                                                                        START_DATE=None,
                                                                                                        END_DATE=None,
                                                                                                        KEY=DOC_ID_GROUP
                                                                                                        ),
                                                        idx=idx_dic[COMPANY_CODE],
                                                        include_rownum_condition=IS_QUERY_WITH_ROWNUM)

            else:
                # 날짜조건 없이 실행
                for COMPANY_CODE in str(loaded_feed_config["feed.compcode.info"]).split(","):

                    # elasticsearch 7.9 default '_doc'
                    OBJ_CONFIG = Bulk.elasticsearch_interface(SYSTEM_ID, idx_dic[COMPANY_CODE], None)

                    result_sets = \
                        get_rows.get_Recordset_Feed(OBJ_CONFIG,
                                                    SYSTEM_ID,
                                                    conn,
                                                    ACTION_FLAG,
                                                    params=Manage_QueryParam.get_system_query_param(SYSTEM_ID, COMPANY_CODE, START_DATE=None, END_DATE=None),
                                                    idx=idx_dic[COMPANY_CODE],
                                                    include_rownum_condition=IS_QUERY_WITH_ROWNUM)

        # @ YYYYMM 날짜수만큼 LOOP DB QUERY 전체건수
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        print(Utils.bcolors().BOLD + Utils.bcolors().YELLOW)
        print('#' * 40)
        print('#' * 40)
        print('Bulk Indexing Search Engine >> {}'.format(ip))
        print('Bulk Indexing SYSTEM_ID >> {}'.format(SYSTEM_ID))
        print('Bulk Indexing Target >> {}'.format(idx_dic))
        print('Bulk Indexing Total Size >> {}'.format(format(get_rows.ROWS_TOTAL_COUNT, ",")))
        print('#' * 40)
        print('#' * 40)
        print(Utils.bcolors().BOLD + Utils.bcolors().ENDC)
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    finally:
        Conn.DB_Transaction_Cls().Set_DB_Disconnect(conn)
        print('\n')
        print(Utils.bcolors().BOLD + Utils.bcolors().YELLOW)
        print('DB Disconnected...')
        print(Utils.bcolors().BOLD + Utils.bcolors().ENDC)

    end_time = datetime.now()

    print('\n')
    print('#'*50)
    print('Feeder Start Time >> {}\nFeeder End Time >> {}'.format(start_time, end_time))
    print('Feeder RunningTime >> {}'.format(end_time - start_time))
    print('#'*50)
    print('\n')

    # ['/ES/ES_Bulk_Incre_Project/ES_Crawled_DB_Bulk.py', 'aa', 'bb', 'cc']
    # print(sys.argv)

    if isTimer.__eq__('T'):
        status = '[FEED DELETE INSERT INCRE_' + str(SYSTEM_ID).upper() + ']'
        print('\n' + Utils.bcolors().BOLD + Utils.bcolors().YELLOW + status + ' Feed Migration Scheduling Start Time >> {}'.format(datetime.datetime.now()))

    # @ File Attach MultiProcessing Queue Kill
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # Queue Creator
    if str(loaded_feed_config['feed.file.use.yn']).__eq__('T'):
        queue = [{'MESSAGE': 'F'}]
        Queue_Transaction.Multiprocessing_Queue_Creator(queue)
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


def main(isTimer, SYSTEM_ID, IS_QUERY_WITH_ROWNUM):
    """

    :param isTimer:
    :param SYSTEM_ID:
    :param IS_QUERY_WITH_ROWNUM:
    :return:
    """

    process_list = []

    # for loop in range(0, 23):
    #     print(loop)
    # exit(1)

    # Get common. feeed. query xml loading..
    Init_Memory.Initialize_Config_Loading(SYSTEM_ID)

    # Feed Memory Config
    loaded_feed_config = Init_Memory.Memory_Feed_Object.get_global_feed_xml_memory()
    # print(loaded_feed_config)
    # exit(1)

    # MultiProcessing Queue -> Socket 파일 GET 후, 텍스트 업데이트
    if str(loaded_feed_config['feed.file.use.yn']).__eq__('T'):

        # DB 접속에 따른 메타 색인
        # 날짜기반으로 DB 쿼리수(PARAMS, COMPANY_CODE, START_DATE, END_DATE)에 따른 메타색인
        p = Process(target=Feed_Meta_Job, args=(isTimer, SYSTEM_ID, IS_QUERY_WITH_ROWNUM,))
        process_list.append(p)
        p.start()

        p = Process(target=Queue_Transaction.Multiprocessing_Queue_Consumer, args=())
        process_list.append(p)
        p.start()

        for proc in process_list:
            proc.join()

    else:
        Feed_Meta_Job(isTimer, SYSTEM_ID, IS_QUERY_WITH_ROWNUM)

    # read_queue.close()
    # read_queue.join_thread()


if __name__ == '__main__':

    # isTimer = 'T'
    isTimer = 'F'

    # print('\nargs >> ', sys.argv)
    # print('\n', sys.argv[0])  # /ES/ES_Feeder_Python/ES_Feeder.py
    # print('\n', sys.argv[1])  # ECM
    # exit(1)

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #  python3.5 /ES/ES_Feeder_Python/ES_Feeder.py ECM
    # SYSTEM_ID = str(sys.argv[1])
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # SYSTEM_ID = 'ECM'
    # SYSTEM_ID = 'ECM_META'
    # SYSTEM_ID = 'ECM_MIGRATION'
    # SYSTEM_ID ='CITIZEN'
    # SYSTEM_ID = 'POSCOMPLY'

    SYSTEM_ID = str(sys.argv[1])
    # SYSTEM_ID = 'test'

    # IS_QUERY_WITH_ROWNUM = True
    IS_QUERY_WITH_ROWNUM = False

    if isTimer.__eq__('T'):
        # schedule.every(10).seconds.do(main, isTimer, SYSTEM_ID)
        # schedule.every(10).minutes.do(main, isTimer, SYSTEM_ID)
        # schedule.every().hour.do(main, isTimer, SYSTEM_ID)
        # schedule.every().day.at("201908:10").do(main, main, isTimer, SYSTEM_ID)
        schedule.every().day.at("23:00").do(main, isTimer, SYSTEM_ID, IS_QUERY_WITH_ROWNUM)
        status = ''

        status = '[FEED DELETE INSERT INCRE_' + str(SYSTEM_ID).upper() + ']'
        print('\n' + Utils.bcolors().BOLD + Utils.bcolors().YELLOW + status + ' Feed Migration Scheduling Start Time >> {}'.format(datetime.datetime.now()))

        while 1:
            schedule.run_pending()

            # status = '[FEED DELETE INSERT INCRE_' + str(SYSTEM_ID).upper() + ']'
            # print('\n' + Utils.bcolors().BOLD + Utils.bcolors().YELLOW + status + ' Feed Migration Scheduling Start Time >> {}'.format(datetime.datetime.now()))
            time.sleep(1)
            # time.sleep(1800)
            # time.sleep(600)
            # time.sleep(10)

    else:
        main(isTimer, SYSTEM_ID, IS_QUERY_WITH_ROWNUM)
