
import calendar

def get_system_query_param(SYSTEM_ID, COMPANY_CODE, START_DATE=None, END_DATE=None, KEY=None):
    """
    idx : posco_bank_version_idx
    [COMPANY_CODE, START_DATE, END_DATE] + [AROWNUM, ROWNUM]
    new_params : ['999', '20200101000000', '20201230235959', 2701, 2800]

    :param SYSTEM_ID:
    :param COMPANY_CODE:
    :param START_DATE:
    :param END_DATE:
    :param KEY:
    :return:
    """

    """
    if START_DATE and END_DATE:
        # START_DATE, END_DATE 마지막날짜 자동 적용 및 hh24miss 덧붙임
        START_DATE = START_DATE + "01000000"
        END_OF_MONTH_DAY = calendar.monthrange(int(str(END_DATE)[:4]), int(str(END_DATE)[4:6]))[1]
        END_DATE = END_DATE + str(END_OF_MONTH_DAY) + "235959"

    # START_DATE = START_DATE + "15000000"
    # END_DATE = END_DATE + "20235959"
    """

    if str(SYSTEM_ID).__eq__('CITIZEN'):
        # return [COMPANY_CODE, START_DATE, END_DATE]
        return [START_DATE, END_DATE]

    elif str(SYSTEM_ID).__eq__('POSCOMPLY'):
        return [COMPANY_CODE]

    # 키리스트
    # ['doc0900bf4ba00eb3e4', 'doc0900bf4ba00e8263', 'doc0900bf4ba01182de', 'doc0900bf4ba00a6ac2', 'doc0900bf4ba00eb3e0',
    #  'doc0900bf4ba011c732', 'doc0900bf4ba007f741', 'doc0900bf4ba007f742', 'doc0900bf4ba007f740']
    elif str(SYSTEM_ID).__eq__('FILE_DOC_ID_ECM'):
        return KEY

    # 공통 파라미터 [COMPANY_CODE, START_DATE, END_DATE]
    else:
        return [COMPANY_CODE, START_DATE, END_DATE]

