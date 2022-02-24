
import jpype
import os

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
            '/ES/ES_Feeder_Python/Lib/DB/ojdbc6.jar',
            '/ES/ES_Feeder_Python/Lib/Feed_Text/Jar/',
            '/ES/ES_Feeder_Python/Lib/Feed_Text/Jar/*.jar',
            '/ES/ES_Feeder_Python/Lib/Feed_Text/Jar/DocumentsTextExtract-import-1.0_lib/*'
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


if __name__ == '__main__':
    init_jvm_environment()