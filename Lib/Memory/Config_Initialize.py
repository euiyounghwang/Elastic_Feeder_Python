
import xml.etree.ElementTree as elemTree
import sys
import os

sys.path.append('/ES/')

from pathlib import Path
import json
import ES_Feeder_Python.Config.getConfig as Config
import ES_Feeder_Python.Lib.Interface.Elastic_API as API
import jpype

# main pysoslsosos
# DEFAULT_FEED_CONFIG_PATH = Path('./Lib/Feed_Config/')
DEFAULT_FEED_CONFIG_PATH = Path(Config.File().get_Root_Directory() + '/ES_Feeder_Python/Lib/Feed_Config/')

# local py
# DEFAULT_FEED_CONFIG_PATH = Path('../Feed_Config/')

Memory_Common_Object = Config.APP_Memory()
Memory_Feed_Object = Config.APP_Memory()
Memory_Query_Object = Config.APP_Memory()

def init_jvm(jvmpath=None, args=None):
    """

    :param jvmpath:
    :param args:
    :return:
    """
    if jpype.isJVMStarted():
        return
    jpype.startJVM(jpype.getDefaultJVMPath(), args)


def init_jvm_environment(jvmpath=None, args=None, max_heap=1024):
    """

    :param jvmpath:
    :param args:
    :return:
    """

    libraries = None
    javadir = []
    installpath = None
    libpaths = []

    if jpype.isJVMStarted():
        return

    # jpype.startJVM(jpype.getDefaultJVMPath(), args)

    javadir = []
    installpath = None
    libpaths = []

    if jpype.isJVMStarted():
        return None

    if not libraries:
        installpath = os.path.dirname(os.path.realpath(__file__))
        print('[installpath] ', installpath)
        libpaths = [
            Config.File().get_Root_Directory() + '/ES_Feeder_Python/Lib/DB/ojdbc6.jar',
            Config.File().get_Root_Directory() + '/ES_Feeder_Python/Lib/Feed_Text/Jar/',
            Config.File().get_Root_Directory() + '/ES_Feeder_Python/Lib/Feed_Text/Jar/*.jar',
            Config.File().get_Root_Directory() + '/ES_Feeder_Python/Lib/Feed_Text/Jar/DocumentsTextExtract-import-1.0_lib/*'
        ]
        javadir = '%s%sjava' % (installpath, os.sep)

    args = [javadir, os.sep]
    libpaths = [p.format(*args) for p in libpaths]

    classpath = os.pathsep.join(f.format(*args) for f in libpaths)
    jvmpath = jpype.getDefaultJVMPath()

    print(libpaths)

    try:
        jpype.startJVM(
            jvmpath,
            '-Djava.class.path=%s' % classpath,
            '-Dfile.encoding=UTF8',
            '-ea', '-Xmx{}m'.format(max_heap)
        )


    except Exception as e:
        print(e)


def Initialize_Config_Loading(SYSTEM_ID):
    """

    :param SYSTEM_ID:
    :return:
    """
    # SYSTEM_ID = 'ECM'
    # SYSTEM_ID = 'CITIZEN'
    # SYSTEM_ID = 'CITIZEN'
    # ECM_DELETED_DATE
    try:
        get_read_config_xml('CONFIG', SYSTEM_ID)

        print('\n\nMemory_Common_Object ', API.elasticserch_utils().pp_json(Memory_Common_Object.get_global_common_xml_memory()))

        if Memory_Feed_Object.get_global_feed_xml_memory():
            print('\n\nMemory_Feed_Object ', API.elasticserch_utils().pp_json( Memory_Feed_Object.get_global_feed_xml_memory()))
            get_read_query_xml('QUERY', SYSTEM_ID)
            print('\n\nMemory_Query_Object ', API.elasticserch_utils().pp_json(Memory_Query_Object.get_global_query_xml_memory()))

    except Exception as ex:
        print('Initialize_Config_Loading <ex> ', ex)


def find_element_common(OPTIONS, root, SYSTEM_ID=None):
    """

    :param OPTIONS:
    :param root:
    :param system_id:
    :return:
    """

    # print('find_element_common ', OPTIONS, SYSTEM_ID)

    memory_dict = {}
    # memory_config_dict = {}
    for child in root.iter():
        if SYSTEM_ID is not None:
            # print('@@@@@@@@', child.attrib.get('id'))
            if str(OPTIONS).__eq__('QUERY'):
                if str(SYSTEM_ID).__eq__(str(child.attrib.get('id'))):
                    for sub_child in child:
                        # print(child.tag, ' >> ', sub_child.tag, sub_child.attrib, child.findtext(sub_child.tag))
                        if len(str(sub_child.text).strip()) > 0:
                            # print(child.tag, ' >> ', sub_child.tag, ' @@ ', sub_child.attrib, ' >> ', str(sub_child.text).strip())
                            memory_dict[sub_child.tag + '_' + sub_child.attrib['id']] = str(sub_child.text).strip()
                            Memory_Query_Object.set_global_query_xml_memory(sub_child.tag + '_' + sub_child.attrib['id'], str(sub_child.text).strip())

            else:
                # print('$$$', child.attrib.get('id'))
                if str(SYSTEM_ID).__eq__(str(child.attrib.get('id'))):
                    for sub_child in child:
                        # print(child.tag, ' >> ', sub_child.tag, sub_child.attrib, child.findtext(sub_child.tag))
                        if len(str(sub_child.text).strip()) > 0:
                            # print(child.tag, ' >> ', sub_child.tag, ' @@ ', sub_child.attrib, ' >> ', str(sub_child.text).strip())
                            memory_dict[sub_child.tag] = str(sub_child.text).strip()
                            Memory_Feed_Object.set_global_feed_xml_memory(sub_child.tag, str(sub_child.text).strip())

        # config common define
        else:
            for sub_child in child:
                # print(child.tag, ' >> ', sub_child.tag, sub_child.attrib, child.findtext(sub_child.tag))
                if len(str(sub_child.text).strip()) > 0:
                    # print(child.tag, ' >> ', sub_child.tag, ' @@ ', sub_child.attrib, ' >> ', str(sub_child.text).strip())
                    memory_dict[sub_child.tag] = str(sub_child.text).strip()
                    Memory_Common_Object.set_global_common_xml_memory(sub_child.tag, str(sub_child.text).strip())


    # print('\n\n')
    if 'query' in memory_dict.keys():
        del(memory_dict['query'])

    # print('memory_dict >> ', API.elasticserch_utils().pp_json(memory_dict))



def get_read_query_xml(OPTIONS, SYSTEM_ID=None):
    """

    :param OPTIONS:
    :param SYSTEM_ID:
    :return:
    """

    tree = elemTree.parse(str(DEFAULT_FEED_CONFIG_PATH) + '/Query.xml')

    # print(OPTIONS, SYSTEM_ID)

    if SYSTEM_ID:
        root = tree.find('./query_map')
        find_element_common(OPTIONS, root, SYSTEM_ID=SYSTEM_ID)


def get_read_config_xml(OPTIONS, SYSTEM_ID):
    """

    :param OPTIONS:
    :param SYSTEM_ID:
    :return:
    """

    print('\nget_read_config_xml -> ', OPTIONS, SYSTEM_ID)

    tree = elemTree.parse(str(DEFAULT_FEED_CONFIG_PATH)+ '/Feed.xml')

    try:
        common = tree.find('./commonInfo')
        find_element_common(OPTIONS, common)

        root = tree.find('./feed_info')
        find_element_common(OPTIONS, root, SYSTEM_ID=SYSTEM_ID)

    except Exception as ex:
        print('ex', ex)



if __name__ == '__main__':
    Initialize_Config_Loading()

