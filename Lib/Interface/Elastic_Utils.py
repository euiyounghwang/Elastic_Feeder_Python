
import json
from multiprocessing import Process, Lock, Queue, Manager, Pool
# from ES_Feeder_Python.Lib.Feed_Text.Process_Queue import *
import ES_Feeder_Python.Config.getConfig as Config
import ES_Feeder_Python.Lib.Feed_Text.Process_Queue as Queue_Transaction


def elasticsearch_response(Indices_Name, StringKeyBuffer, results_list):
    """
    response elasticsearch 7.X version
    :param Indices_Name:
    :param StringKeyBuffer:
    :param results_list:
    :return:
    """
    print('\n\nelasticsearch_response function called..')
    # print(results)


    response_ack = []
    feed_sum_indexing_count , feed_success_total_count, feed_fail_total_count = 0, 0, 0

    queue = []

    if results_list:
        # print('\nresults', results_list)
        for rows in results_list:
            # print('row', rows)
            each_row = json.loads(rows)

            if 'index' in each_row:
                if str(each_row['index']['status']).__contains__('2'):
                    response_ack.append('[CS] ' + each_row['index']['_id'])
                    feed_success_total_count += 1
                else:
                    # log.error('curl_file_command -> index' + ' >> ' + results)
                    response_ack.append('[CF] ' + each_row['index']['_id'])
                    feed_fail_total_count += 1

            elif 'update' in each_row:
                if str(each_row['update']['status']).__contains__('2'):
                    response_ack.append('[US] ' + each_row['update']['_id'])
                    feed_success_total_count += 1

                    # queue creator
                    '''
                    self.StringKeyBuffer = {
                        str(rows['KEY']): str(rows['KEY']),
                        'VERSION': str(rows['VERSION']),
                        'OPERATION': 'doc'
                    }
                    '''

                    # add_meta 에서 VERSION 칼럼이 있는경우 처리
                    # StringKeyBuffer >>  {'doc0900bf4b9f0681dd': 'doc0900bf4b9f0681dd', 'VERSION': '0900bf4b9f0681dd', 'OPERATION': 'doc'}
                    # print('\nStringKeyBuffer >> ', StringKeyBuffer)
                    if each_row['update']['_id'] in dict(StringKeyBuffer).keys():
                        # print('OK', each_row['update']['_id'])
                        queue_dic = {
                            'SYS_ID': str(dict(StringKeyBuffer)['OPERATION']),
                            # 'MESSAGE': Indices_Name + ';' + each_row['update']['_id'] + ',' + StringKeyBuffer[each_row['update']['_id']]
                            'MESSAGE': Indices_Name + ';' + each_row['update']['_id'] + ',' + str(dict(StringKeyBuffer)[each_row['update']['_id']])
                        }
                        # print('queue_dic', queue_dic)
                        queue.append(queue_dic)

                        # del StringKeyBuffer
                        del dict(StringKeyBuffer)[each_row['update']['_id']]

                else:
                    # log.error('curl_file_command -> index' + ' >> ' + results)
                    response_ack.append('[UF] ' + each_row['update']['_id'])
                    feed_fail_total_count += 1

            elif 'delete' in each_row:
                if str(each_row['delete']['status']).__contains__('2'):
                    response_ack.append('[DS] ' + each_row['delete']['_id'])
                    feed_success_total_count += 1
                else:
                    # log.error('curl_file_command -> index' + ' >> ' + results)
                    print('@@@', each_row[1])
                    response_ack.append('[DF] ' + each_row['delete']['_id'])
                    feed_fail_total_count += 1

            feed_sum_indexing_count += 1

        # Queue Creator
        # Queue_Transaction.Multiprocessing_Queue_Creator(''.join(queue))
        # print('\nQueue_Transaction.Multiprocessing_Queue_Creator(queue)', queue)
        # 첨부파일 처리 것만 큐에 쌓고 첨부업데이트 결과는 Queue에 다시 들어가면 안됨
        if dict(StringKeyBuffer):
            Queue_Transaction.Multiprocessing_Queue_Creator(queue)

    print('\nresults >> ', ' '.join(response_ack))

    return feed_success_total_count, feed_fail_total_count, feed_sum_indexing_count


if __name__ == '__main__':
    response_list = []
    response_list.append(json.dumps({'index': {'_shards': {'total': 2, 'successful': 2, 'failed': 0}, '_index': 'bank_version1', 'forced_refresh': True, '_seq_no': 49559, '_id': 'CU_pAHQB0wDKL2WMW8HX', '_version': 1, '_type': '_doc', 'result': 'created', 'status': 201, '_primary_term': 1}}))
    response_list.append(json.dumps({'index': {'_shards': {'total': 2, 'successful': 2, 'failed': 0}, '_index': 'bank_version1', 'forced_refresh': True, '_seq_no': 49559, '_id': 'CU_pAHQB0wDKL2WMW8HX', '_version': 1, '_type': '_doc', 'result': 'created', 'status': 201, '_primary_term': 1}}))
    # data = json.loads(response)
    # data = json.dumps(response)
    print('response_list ', response_list)
    print(elasticsearch_response(response_list))
