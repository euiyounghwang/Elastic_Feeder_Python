# -*- coding: utf-8 -*-

import os
import ES_Feeder_Python.Lib.Feed_Text.SSH.SSH_Control as SSH_Controls
import ES_Feeder_Python.Lib.Util.Util as Utils
import ES_Feeder_Python.Lib.Logging.Logging as log

class SSH_Function_Class:

   def __init__(self, server_ip, server_id, server_passwd, local_file_path, target_file_path):
      """

      :param server_ip:
      :param server_id:
      :param server_passwd:
      :param local_file_path:
      :param target_file_path:
      """
      self.server_ip = server_ip
      self.server_port = 22
      self.server_id = server_id
      self.server_passwd = server_passwd

      # self.ssh = SSH_Controls.get_ssh(self.server_ip, self.server_port, self.server_id, self.server_passwd)
      self.ssh = None
      self.sftp = None

      self.target_file_path = target_file_path
      self.local_file_path = local_file_path


   def Get_SSH_Connection(self):
      """

      :return:
      """
      if self.ssh is None and self.sftp is None:
         self.ssh = SSH_Controls.get_ssh(self.server_ip, self.server_port, self.server_id, self.server_passwd)
         self.sftp = SSH_Controls.get_sftp(self.ssh)

      # return ssh, sftp


   def Set_SSH_Disconnection(self):
      """

      :param ssh:
      :param sftp:
      :return:
      """
      SSH_Controls.close_sftp(self.sftp)
      SSH_Controls.close_ssh(self.ssh)


   def SSH_Invoke_FileUpload(self):
      """

      :return:
      """
      file_list = os.listdir(self.local_file_path)
      file_list.sort()

      # ssh = SSH_Controls.get_ssh("10.132.12.90", 22, "tomadmt", "posco123")

      # exitcode = SSH_Controls.ssh_execute(ssh, "ls " + TARGT_UPLOAD_PATH + " -al")
      # print("result : %d" % exitcode)

      # sftp = SSH_Controls.get_sftp(ssh)
      for item in file_list:
         SSH_Controls.file_upload(self.sftp, self.local_file_path + item, self.target_file_path + item)

      #file_download(sftp, Define.SSH().source_upload_path + "2018010221252516799CDA28AE79D2B8EEDF1D43AC4D0CF00.node_pur24.723010232802715E9.pdf", Define.SSH().target_upload_path + "2018010221252516799CDA28AE79D2B8EEDF1D43AC4D0CF00.node_pur24.723010232802715E9.pdf")
      #exitcode=ssh_execute(ssh, "ls " + Define.SSH().target_upload_path + " -laR")

      # exitcode = SSH_Controls.ssh_execute(ssh, "ls " + TARGT_UPLOAD_PATH + " -al")
      # print("result : %d" % exitcode)

      # SSH_Controls.close_ssh(ssh)
      # SSH_Controls.close_sftp(sftp)



   def SSH_Invoke_FileDownload(self, download_file):
      """

      :param dwonload_file:
      :return:
      """
      # ssh = SSH_Controls.get_ssh("10.132.12.90", 22, "tomadmt", "posco123")

      # exitcode = SSH_Controls.ssh_execute(ssh, "ls " + TARGT_UPLOAD_PATH + " -al")
      # print("result : %d" % exitcode)

      # sftp = SSH_Controls.get_sftp(ssh)

      SSH_Controls.file_download(self.sftp, self.local_file_path + download_file, self.target_file_path + download_file)

      # exitcode = SSH_Controls.ssh_execute(ssh, "ls " + LOCAL_UPLOAD_PATH + " -al")
      # print("result : %d" % exitcode)

      # SSH_Controls.close_ssh(ssh)
      # SSH_Controls.close_sftp(sftp)



   def SSH_Invoke_FileDelete(self, dest_path):
      """
      :param dest_path:
      :return:
      """

      try:
         self.sftp.remove(dest_path)
         # print("\nSuccess to Delete  " + dest_path)
         log.info(Utils.bcolors().BOLD + Utils.bcolors().YELLOW + 'Success to Local File DELETE => {!r} '.format(dest_path) + Utils.bcolors().ENDC)

      except Exception as ex:  # 에러 종류
         log.error(Utils.bcolors().BOLD + Utils.bcolors().YELLOW + 'Fail to Local File DELETE => {!r} '.format(dest_path) + Utils.bcolors().ENDC)

if __name__ == '__main__':

   LOCAL_UPLOAD_PATH = '/ES/download_test/'
   TARGT_SERVER_PATH = '/TOM/ECM_Delegate/dec_files/'

   SERVER_IP = "10.132.12.90"
   SERVER_ID = "tomadmt"
   SERVER_PW = "posco123"

   try:

      SSH_OBJ = SSH_Function_Class(SERVER_IP, SERVER_ID, SERVER_PW, LOCAL_UPLOAD_PATH, TARGT_SERVER_PATH)

      SSH_OBJ.Get_SSH_Connection()
      SSH_OBJ.SSH_Invoke_FileUpload()

      download_file = '1.pptx'
      SSH_OBJ.SSH_Invoke_FileDownload(download_file)

      # dest_path_file = TARGT_SERVER_PATH + 'tmp_ECM_0900bf4b9fb9c6fa_0900bf4b9fb9c6fa_1600789271621.xlsx'
      # SSH_OBJ.SSH_Invoke_FileDelete(dest_path_file)

   finally:
      SSH_OBJ.Set_SSH_Disconnection()
