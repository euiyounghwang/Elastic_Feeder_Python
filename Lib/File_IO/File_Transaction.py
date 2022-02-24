
# PATH = '/ES/ES_Feeder_Python/Input/ECM_DOC_ID_LIST'
PATH = '/ES/ES_Feeder_Python/Input/TEST'

def file_doc_id_list():
    """

    :return:
    """
    doc_id_list = []
    with open(PATH, 'r+', encoding='utf-8') as object_id_files:
        while True:
            line = object_id_files.readline()
            # if len(line) == 0:
            if not line:
                break

            doc_id_list.append(str(line).replace('\n', ''))

    print('\n\n')
    # print('object_id_list ', object_id_list)

    return doc_id_list


if __name__ == '__main__':
    print('\n')
    print(file_doc_id_list())
    print('Max ', len(file_doc_id_list()))

    Max_In_Size = 10
    print(len(file_doc_id_list())/Max_In_Size, int(len(file_doc_id_list())/Max_In_Size)+1)

    for loop in range(0, int(len(file_doc_id_list())/Max_In_Size)+1):
        # KEY_LIST = "','".join(file_doc_id_list()[loop*Max_In_Size:(loop*Max_In_Size)+Max_In_Size])
        # print(loop, "'" + KEY_LIST + "'")
        current_doc_list = file_doc_id_list()[loop*Max_In_Size:(loop*Max_In_Size)+Max_In_Size]

        if current_doc_list:
            print('OK1?', current_doc_list)
            print('\n###')
            print('OK2?', ','.join(current_doc_list))
            print('\n###')
            print(",".join(map(str,current_doc_list)))
            print('\n###')
            print( "' OR ".join(("A.ECM_DOC_ID = '" + str(n) for n in current_doc_list)))
