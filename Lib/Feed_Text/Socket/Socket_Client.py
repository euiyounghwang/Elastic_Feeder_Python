import socket
import sys
import os

sys.path.append(os.getcwd())

import ES_Feeder_Python.Lib.Util.Util as Utils
import ES_Feeder_Python.Lib.Logging.Logging as log
from ES_Feeder_Python.Lib.Feed_Text.SSH.SSH_Invoke import *
import ES_Feeder_Python.Lib.Feed_Text.Gather_Text as Full_Text
from ES_Feeder_Python.Lib.Memory import Config_Initialize

def getSokcetTimeout(IP, PORT):
    """

    :param IP:
    :param PORT:
    :return:
    """

    try:
        # Create a TCP/IP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        # server_address = ('10.132.12.89', 8191)
        server_address = (str(IP), PORT)
        log.info(Utils.bcolors().BOLD + Utils.bcolors().YELLOW + 'Connecting to Port => {!r} '.format(*server_address) + Utils.bcolors().ENDC)
        # print('connecting to {} port {}'.format(*server_address))

        client_socket.connect(server_address)

        return client_socket

    except Exception as ex:  # 에러 종류
        print('getSokcetTimeout >> ' + ex)


def getSocket_RemoteDownload(file_name, default_view,
                             SERVER_IP='127.0.0.1',
                             SERVER_PORT=8191,
                             SERVER_ID='account',
                             SERVER_PW = 'passwd',
                             LOCAL_UPLOAD_PATH='/home/download_test/',
                             TARGT_SERVER_PATH = '/dec_files/',
                             REMOTE_USE_Y_N='T'
                             ):

    """
    Test SSH Default Info
    :param file_name:
    :param default_view:
    :param SERVER_IP:
    :param SERVER_PORT:
    :param SERVER_ID:
    :param SERVER_PW:
    :param LOCAL_UPLOAD_PATH:
    :param TARGT_SERVER_PATH:
    :param REMOTE_USE_Y_N:
    :return:
    """

    import ES_Feeder_Python.Lib.Memory.Config_Initialize as Init_Memory
    loaded_feed_config = Init_Memory.Memory_Feed_Object.get_global_feed_xml_memory()

    SSH_OBJ = None

    # file download
    # 실제 Feed 정상실행 시 메모리에 올라와있음
    if loaded_feed_config:
        ssh_info_dic = {
            'ssh_server_ip': str(loaded_feed_config['feed.file.server.ip']),
            'ssh_server_port': int(loaded_feed_config['feed.file.server.port']),
            'ssh_server_id': str(loaded_feed_config['feed.file.sever.id']),
            'ssh_server_pwd': str(loaded_feed_config['feed.file.sever.pw']),
            'ssh_server_local_path': str(loaded_feed_config['feed.local.path']),
            'ssh_server_target_path': str(loaded_feed_config['feed.target.path'])
        }
        LOCAL_UPLOAD_PATH = str(loaded_feed_config['feed.local.path'])
        REMOTE_USE_Y_N = str(loaded_feed_config['feed.remote_file.use.yn'])

    else:
        ssh_info_dic = {
            'ssh_server_ip': SERVER_IP,
            'ssh_server_port': SERVER_PORT,
            'ssh_server_id': SERVER_ID,
            'ssh_server_pwd': SERVER_PW,
            'ssh_server_local_path': LOCAL_UPLOAD_PATH,
            'ssh_server_target_path': TARGT_SERVER_PATH
        }

    try:

        # 'feed.remote_file.use.yn' Y 일 경우
        if str(REMOTE_USE_Y_N).__eq__('T'):

            # is_enable_SSH = True
            is_enable_SSH = False

            # SSH
            if is_enable_SSH:
                # print('file_name >> ', file_name)
                SSH_OBJ = SSH_Function_Class(ssh_info_dic['ssh_server_ip'],
                                             ssh_info_dic['ssh_server_id'],
                                             ssh_info_dic['ssh_server_pwd'],
                                             ssh_info_dic['ssh_server_local_path'],
                                             ssh_info_dic['ssh_server_target_path']
                                             )
                SSH_OBJ.Get_SSH_Connection()

                # SSH_OBJ.SSH_Invoke_FileUpload()
                #
                # download_file = '1.pptx'
                file_name = str(file_name).split(";")[1].replace("\n", "")
                SSH_OBJ.SSH_Invoke_FileDownload(file_name)

                # REMOTE DELETE FILE
                dest_path_file = TARGT_SERVER_PATH + file_name
                SSH_OBJ.SSH_Invoke_FileDelete(dest_path_file)

            # SCP Keygen
            else:

                file_name = str(file_name).split(";")[1].replace("\n", "")

                # remote download
                # os.system('scp tomadmd@10.132.18.170:/TOM/1.pptx /ES/ES_Feeder_Python/Lib/Feed_Text/')
                os.system('scp {}@{}:{} {}'.format(str(ssh_info_dic['ssh_server_id']),
                                                   str(ssh_info_dic['ssh_server_ip']),
                                                   str(ssh_info_dic['ssh_server_target_path']) + file_name,
                                                   str(ssh_info_dic['ssh_server_local_path'] + file_name)
                                                   ))

                # remote delete
                # os.system('ssh tomadmt@10.132.12.90 -p22 "rm -rf /TOM/TEST/1.pptx"')
                os.system('ssh {}@{} -p22 "rm -rf {}"'.format(str(ssh_info_dic['ssh_server_id']),
                                                              str(ssh_info_dic['ssh_server_ip']),
                                                              str(ssh_info_dic['ssh_server_target_path'] + file_name)
                                                              ))
        else:
            file_name = str(file_name).split(";")[1].replace("\n", "")

        # Gather Text
        return SSH_OBJ, Full_Text.Call_Jar_Text(LOCAL_UPLOAD_PATH + file_name, default_view)

    except Exception as ex:  # 에러 종류
        # print('Call_Jar_Text >> ' + ex)
        pass

    finally:

        try:
            # if is_enable_SSH:
                # 한번만 계정실행 -> 마지막에 상위에서 종료
                # SSH_OBJ.Set_SSH_Disconnection()

            # After Gather Text -> LOCAL 파일 삭제
            # os.remove(LOCAL_UPLOAD_PATH + file_name)
            if os.path.exists(LOCAL_UPLOAD_PATH + file_name):
                os.remove(LOCAL_UPLOAD_PATH + file_name)

            """
            # remote delete
            # os.system('ssh tomadmt@10.132.12.90 -p22 "rm -rf /TOM/TEST/1.pptx"')
            os.system('ssh {}@{} -p22 "rm -rf {}"'.format(str(ssh_info_dic['ssh_server_id']),
                                                          str(ssh_info_dic['ssh_server_ip']),
                                                          str(ssh_info_dic['ssh_server_target_path'] + file_name)
                                                          ))
            """

        except Exception as ex:  # 에러 종류
            # print('Call_Jar_Text >> ' + ex)
            pass



def getSocketSend(client_socket, message, default_view=True):
    """
    Java Socket Server : message = 'ECM;0900bf4b9fb9c6fa\n'  (ECM)
    Java Socket Server : message = 'ftp_download;/array5/image/ipspro/2008630_36.pdf\n'  (FTP)
    :param client_socket:
    :param message:
    :return:
    """
    try:
        log.info(Utils.bcolors().BOLD + Utils.bcolors().YELLOW + 'Send => {!r}'.format(message) + Utils.bcolors().ENDC)
        sbuff = bytes(message, encoding='utf-8')
        client_socket.send(sbuff)

        rbuff = client_socket.recv(1024).decode()
        received = str(rbuff)
        log.info(Utils.bcolors().BOLD + Utils.bcolors().YELLOW + 'Received => {!r}'.format(received) + Utils.bcolors().ENDC)

        if received:
            # Received = > 'E!File Not Found\n'
            if not str(received).__contains__('E!'):
                if str(received).__contains__('S;'):
                    return getSocket_RemoteDownload(received, default_view)
                else:
                    return None, ""
            else:
                return None, ""
    finally:
        log.info(Utils.bcolors().BOLD + Utils.bcolors().YELLOW + 'Socket Closed..' + Utils.bcolors().ENDC)
        # message = 'F'
        # # print('sending {!r}'.format(message))
        # client_socket.sendall(message.encode('utf-8'))
        # client_socket.close()
        # return None, ""


if __name__ == '__main__':
    # ******************************************************************************************************
    # ******************************************************************************************************
    # ******************************************************************************************************
    # Feed Initialize
    Config_Initialize.Memory_Common_Object.set_global_common_xml_memory('feed.file.limit.size', '104857600')
    # Feed Initialize
    Config_Initialize.Memory_Feed_Object.set_global_feed_xml_memory('feed.file.server.ip', '127.0.0.1')
    Config_Initialize.Memory_Feed_Object.set_global_feed_xml_memory('feed.file.server.port', 8191)
    Config_Initialize.Memory_Feed_Object.set_global_feed_xml_memory('feed.file.sever.id', 'account')
    Config_Initialize.Memory_Feed_Object.set_global_feed_xml_memory('feed.file.sever.pw', 'passwd')
    Config_Initialize.Memory_Feed_Object.set_global_feed_xml_memory('feed.local.path', '/ES/download_test/')
    Config_Initialize.Memory_Feed_Object.set_global_feed_xml_memory('feed.target.path', '/dec_files/')
    Config_Initialize.Memory_Feed_Object.set_global_feed_xml_memory('feed.file.use.yn', 'T')
    Config_Initialize.Memory_Feed_Object.set_global_feed_xml_memory('feed.remote_file.use.yn', 'T')
    # ******************************************************************************************************
    # ******************************************************************************************************
    # ******************************************************************************************************

    from threading import Thread
    SOCKET_SERVER_IP = str(Config_Initialize.Memory_Feed_Object.get_global_feed_xml_memory()['feed.file.server.ip'])
    client_socket = getSokcetTimeout(SOCKET_SERVER_IP, int(Config_Initialize.Memory_Feed_Object.get_global_feed_xml_memory()['feed.file.server.port']))
    """
    getSocketSend(client_socket, msg)
    # Thread(target=getSocketSend, args=(client_socket, msg)).start()
    message = 'F'
    client_socket.sendall(message.encode('utf-8'))
    client_socket.close()
    """

    msg = 'DOC;0900bf4b9816277d\n'
    SSH_OBJ, full_contents = getSocketSend(client_socket, msg)

    message = 'F'
    client_socket.sendall(message.encode('utf-8'))
    client_socket.close()





