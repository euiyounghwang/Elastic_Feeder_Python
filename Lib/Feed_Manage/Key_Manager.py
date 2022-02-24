

import time
import datetime

POSCO_ECM_GRP_IDX = 'test_ecm_grp'

def set_key_value(key):
    """
     KEY: 3456.0
    :param self:
    :param key:
    :return:
    """

    if str(key).replace('.0', '').isdigit():
        return str(key).replace('.0', '')
    else:
        return str(key)


def set_key_idx_name(idx, rows):
    """

    :param self:
    :param idx:
    :param rows:
    :return:
    """

    from datetime import datetime

    """
    print('@@@@@@@@@@@@@@@@@')
    print('@@@@@@@@@@@@@@@@@')
    print('\nidx', idx)
    print('\nrows', rows)
    print('@@@@@@@@@@@@@@@@@')
    print('@@@@@@@@@@@@@@@@@')
    """

    DATE_CONDITION = '%Y-%m-%d %H:%M:%S'

    # print('\n\n\n###rows', rows['INPUTDATE'])

    # POSCO_ECM_GRP IDX CHECK
    if str(idx).__contains__(POSCO_ECM_GRP_IDX):

        input_dt = datetime.strptime(rows['INPUTDATE'], DATE_CONDITION)

        if input_dt < datetime.strptime('2013-01-01 00:00:00', DATE_CONDITION):
            return 'test_ecm_grp1_idx'

        elif (input_dt >= datetime.strptime('2013-01-01 00:00:00', DATE_CONDITION)) \
                and (input_dt < datetime.strptime('2017-01-01 00:00:00', DATE_CONDITION)):
            return 'test_ecm_grp2_idx'

        elif (input_dt >= datetime.strptime('2017-01-01 00:00:00', DATE_CONDITION)) \
                and (input_dt < datetime.strptime('2018-01-01 00:00:00', DATE_CONDITION)):
            return 'test_ecm_grp3_idx'

        elif (input_dt >= datetime.strptime('2018-01-01 00:00:00', DATE_CONDITION)) \
                and (input_dt < datetime.strptime('2020-01-01 00:00:00', DATE_CONDITION)):
            return 'test_ecm_grp4_idx'

        elif input_dt >= datetime.strptime('2020-01-01 00:00:00', DATE_CONDITION):
            return 'test_ecm_grp5_idx'

    else:
        # print('else')
        return str(idx)

