
import subprocess as sub
import os
import jpype
import ES_Feeder_Python.Lib.Util.Util as Utils
import ES_Feeder_Python.Lib.Logging.Logging as log
import ES_Feeder_Python.Lib.Feed_Text.library.Tika_Python_Func as TiKa

PATH  = '/ES/ES_Feeder_Python/Lib/Feed_Text/'


def Call_Jar_Text_Bkp(doc, Text_More_Not_Custormized):
    """
    Text_More_Not_Custormized = 'true'
    Text_More_Not_Custormized = 'false'
    :param doc:
    :param Text_More_Not_Custormized:
    :return:
    """

    try:

        # Class Call
        # import jpype
        #
        # jpype.startJVM(jpype.getDefaultJVMPath(), '-ae', "-Djava.class.path=" + PATH + "/Jar/DocumentsTextExtract-import-1.0.jar")
        # pkg = jpype.JPackage('Documents.Office.Poi')
        # javaobj = pkg.ApachePoiTextRead(doc)
        # gather_contents = javaobj.Common_Original_TextMain()
        #
        # log.info(Utils.bcolors().BOLD + Utils.bcolors().YELLOW + 'Call_Jar_Text ... ' + '\n\n'.join(str(gather_contents).split('\n')) + Utils.bcolors().ENDC)
        # print('\n\n')


        log.info(Utils.bcolors().BOLD + Utils.bcolors().YELLOW + 'Call_Jar_Text ... ' + Utils.bcolors().ENDC)
        print('@@@@@@@@@@@', doc)
        # get_contents = sub.call(['java', '-jar', PATH + "/Jar/DocumentsTextExtract-import-1.0.jar", doc])
        sub.call(['java', '-jar', PATH + "/Jar/DocumentsTextExtract-import-1.0.jar", doc, Text_More_Not_Custormized])
        # print('\n')


        # print("#######", os.path.split(doc))
        # os.path.split(doc) => ('/ES/download_test', 'tmp_ECM_0900bf4b9a79799f_0900bf4b9a79799f_1601199995612.pdf')
        from os.path import dirname
        from os.path import basename

        # print('1)', dirname(doc))
        # print('2)', basename(doc))

        real_extracted_file_name = str(basename(doc))
        if str(real_extracted_file_name).__contains__("."):
            real_extracted_file_name = str(real_extracted_file_name).split(".")[0]
        else:
            real_extracted_file_name = str(basename(doc))

        # print('3)', str(dirname(doc)))
        # print('4)', real_extracted_file_name)
        REAL_FILE_PATH = str(dirname(doc)) + "/" + str(real_extracted_file_name)
        # REAL_FILE_PATH = str(dirname(doc)) + "/" + str(basename(doc))
        log.info(Utils.bcolors().BOLD + Utils.bcolors().YELLOW + 'REAL_FILE_PATH => {} '.format(REAL_FILE_PATH) + Utils.bcolors().ENDC)
        with open(REAL_FILE_PATH, "r") as input:
            gather_contents = input.read()

        # gather_contents = str(gather_contents).replace('〈개선 후 주요구성 또는 기술적 수단 기재〉','')
        # gather_contents = str(gather_contents)[:100]

        log.info(Utils.bcolors().BOLD + Utils.bcolors().YELLOW + '[{}] Extract Text => {} '.format(real_extracted_file_name, '\n\n'.join(str(gather_contents).split('\n'))) + Utils.bcolors().ENDC)
        os.remove(REAL_FILE_PATH)
        log.info(Utils.bcolors().BOLD + Utils.bcolors().YELLOW + ' Converted Text Delete => {} '.format(REAL_FILE_PATH) + Utils.bcolors().ENDC)

    except Exception as ex:  # 에러 종류
         print('Call_Jar_Text >> ' + ex)

def Call_Jar_Text(doc, default_view):
    """
    Text_More_Not_Custormized = 'true'
    Text_More_Not_Custormized = 'false'
    :param doc:
    :param Text_More_Not_Custormized:
    :return:
    """

    try:

        import ES_Feeder_Python.Lib.Memory.Config_Initialize as Init_Memory
        loaded_common_config = Init_Memory.Memory_Common_Object.get_global_common_xml_memory()

        if not loaded_common_config:
            loaded_common_config.update({'feed.file.limit.size' : '104857600'})

        # Class Call
        import jpype

        if not jpype.isJVMStarted():
            log.info('@@@@@@@ not jpype.isJVMStarted() .. Retry.. @@@@@@')
            jpype.startJVM(jpype.getDefaultJVMPath(), '-ae', "-Djava.class.path=" + PATH + "/Jar/DocumentsTextExtract-import-1.0.jar")

        log.info('START...')
        log.info('doc >> ' + doc + ' [' + str(os.path.getsize(doc)) + ']')

        if float(os.path.getsize(doc)) > float(loaded_common_config['feed.file.limit.size']):
            return ""

        ## PPTX ERROR
        # 0900bf4b9ef05d6d -> 0900bf4b9ef78707
        if str(doc).__contains__('.pptx'):
            gather_contents = TiKa.Tika_office2007_PPTX_Parser(doc)
        # elif str(doc).__contains__('.xlsx'):
        #     gather_contents = TiKa.Tika_office_XLSX_Parser(doc)
        else:
            pkg = jpype.JPackage('Documents.Office.Poi')
            javaobj = pkg.ApachePoiTextRead(doc)
            # gather_contents = javaobj.Common_Original_TextMain()
            gather_contents = javaobj.CommonTextMain()

        if default_view:
            log.info(Utils.bcolors().BOLD + Utils.bcolors().YELLOW + 'Call_Jar_Text ... ' + str(gather_contents) + Utils.bcolors().ENDC)

        return str(gather_contents).replace('None','')

    except Exception as ex:  # 에러 종류
         print('Call_Jar_Text >> ' + ex)
         pass

    finally:
        log.info('Finished...')



if __name__ == '__main__':
    # doc = '/ES/ADSP_Summary.pdf'
    # doc = '/ES/JEAN.doc'
    # doc = '/ES/Sample1.doc'
    doc = '/home/GATHER_TEXT/[Sample] #6.pdf'
    # doc = '/ES/download_test/tmp_ECM_0900bf4b9efb7136_0900bf4b9efb7136_1607798011188.pptx'
    Call_Jar_Text(doc, default_view=True)
