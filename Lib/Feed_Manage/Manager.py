
import time
import datetime

import ES_Feeder_Python.Lib.Memory.Config_Initialize as Init_Memory


def INIT_DELETE_IDX(system_classfy, idx_dic):
    """
    
    :param system_classfy: 
    :param idx: 
    :return: 
    """
    print('\nInitialze_delete_all_idx ', system_classfy, idx_dic)


def get_manipulate_idx(system_classfy, idx):
    """

    :param system_classfy:
    :param idx:
    :return:
    """

    common_prefix_naming = {}
    idx_list_dic = {}

    # print('get_manipulate_idx >> ', idx)
    COMPANY_CODE = Init_Memory.Memory_Feed_Object.get_global_feed_xml_memory()["feed.compcode.info"]

    # 날짜형태가 idx명 + 처리 (록된 회사코드수만큼)
    if str(idx).__contains__('YYYY-MM'):
        idx = str(idx).replace('YYYY-MM', '') + (datetime.date.today() - datetime.timedelta(days=2)).strftime("%Y-%m")

        multi_company_code = str(COMPANY_CODE).split(",")
        for code in multi_company_code:
            idx_list_dic[code] = idx

    #_idx 이름 -> posco,ict,pnr 등의 naming을 등록된 회사코드수만큼 붙여줌
    # *_ecm_grp_idx => posco_ecm_grp_idx, ict_ecm_grp_idx, pnr_ecm_grp_idx ..
    elif str(idx).__contains__('*'):
        print('get_manipulate_idx >> ', idx)
        print('company_code', COMPANY_CODE)
        print('common', Init_Memory.Memory_Common_Object.get_global_common_xml_memory())

        COMPANY_CODE_LIST = str(Init_Memory.Memory_Common_Object.get_global_common_xml_memory()["feed.company.code"])
        COMPANY_NAME_LIST = str(Init_Memory.Memory_Common_Object.get_global_common_xml_memory()["feed.company.name"])

        for loop in range(0, len(COMPANY_CODE_LIST.split(","))):
            common_prefix_naming[COMPANY_CODE_LIST.split(",")[loop]] = str(COMPANY_NAME_LIST.split(",")[loop]).lower()

        # Feed.xml 등록된 회사코드수,  회사코드에 대한 idx명
        multi_company_code = str(COMPANY_CODE).split(",")
        for code in multi_company_code:
            # print('code ', code, 'common_prefix_naming[code] ', common_prefix_naming[code])
            new_idx = str(idx).replace("*", common_prefix_naming[code])
            idx_list_dic[code] = new_idx

        print('\n\n')
        # print('common_prefix_naming', common_prefix_naming)
        # idx = str(idx).replace("*", common_prefix_naming[COMPANY_CODE])
        print("idx", idx)

    # 공통 파라미터 [COMPANY_CODE, START_DATE, END_DATE] -> 동일 idx명으로 등록된 회사코드수만큼 처리
    else:
        multi_company_code = str(COMPANY_CODE).split(",")
        for code in multi_company_code:
            idx_list_dic[code] = idx

    print('idx_list_dic ', idx_list_dic)

    return idx_list_dic

