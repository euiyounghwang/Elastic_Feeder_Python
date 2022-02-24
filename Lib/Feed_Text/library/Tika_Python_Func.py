
from tika import parser
import jpype

PATH  = '/ES/ES_Feeder_Python/Lib/Feed_Text/'

# PATH = '/ES/download_test/tmp_ECM_0900bf4b9ef05d6d_0900bf4b9ef05d6d_1608268096033.pptx'
# PATH = '/ES/191203_E.pptx'

def Tika_office2007_PPTX_Parser(doc):
    """

    :param doc:
    :return:
    """
    from pptx import Presentation
    prs = Presentation(doc)
    result = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for paragraph in shape.text_frame.paragraphs:
                result.append(paragraph.text)
    # print(' '.join(result))

    if not jpype.isJVMStarted():
        jpype.startJVM(jpype.getDefaultJVMPath(), '-ae', "-Djava.class.path=" + PATH + "/Jar/DocumentsTextExtract-import-1.0.jar")

    pkg = jpype.JPackage('Documents.Office.Poi')
    javaobj = pkg.ApachePoiTextRead(doc)
    # gather_contents = javaobj.Common_Original_TextMain()
    gather_contents = javaobj.TruncatedTextExtract(' '.join(result))
    # print('\n\n')
    # print(gather_contents)
    return gather_contents


def Tika_CSV_Parser(doc):
    """

    :param doc:
    :return:
    """
    import csv
    extracted_text = []

    with open(doc) as File:
        reader = csv.reader(File, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            # print(row)
            extracted_text.extend(row)

    # print('@@', ','.join(extracted_text))

    """
    import pandas as pd
    df = pd.read_csv(doc, sep=',', encoding='utf-8')
    # print(df.columns)
    # print(df.head())
    # print(df.shape)
    # print(df.to_string)
    loop = 1
    # for row_index, row in df.iterrows():
    #     print(row_index)
    #     print(row)
    print('@@', df.info())
    for column in df.columns:
        # print(column, df[column].values.tolist())
        extracted_text.extend(df[column].values.tolist())
        # print(extracted_text)

    print(list(set(extracted_text)), type(extracted_text))
    # print(extracted_text)
    """

    if not jpype.isJVMStarted():
        jpype.startJVM(jpype.getDefaultJVMPath(), '-ae', "-Djava.class.path=" + PATH + "/Jar/DocumentsTextExtract-import-1.0.jar")

    pkg = jpype.JPackage('Documents.Office.Poi')
    javaobj = pkg.ApachePoiTextRead(doc)
    # gather_contents = javaobj.Common_Original_TextMain()
    gather_contents = javaobj.TruncatedTextExtract(','.join(extracted_text))

    return gather_contents


def Tika_office2007_XLS_Parser(doc):
    """

    :param doc:
    :return:
    """
    '''
    import pandas as pd
    df = pd.read_excel(doc)
    print(df.head(10))
    '''
    import pandas as pd
    (df,) = pd.read_html(doc, encoding='utf-8')
    # df = pd.read_html(doc)
    # print(df[0], '@@', len(df))
    contents = []
    for i, value in enumerate(df):
        contents.extend(df[i])

    # print('@@', list(set(contents)))
    import math
    extracted_text = list(set(contents))
    n = len(extracted_text)
    j = -1
    for i in range(n):
        j += 1
        if not isinstance(extracted_text[j], str) and math.isnan(extracted_text[j]):
            del extracted_text[j]
            j = j - 1
    print(' '.join(extracted_text))


if __name__ == '__main__':
    # print('\n\n')
    # print(Tika_office2007_PPTX_Parser('/ES/191203_E.pptx'))
    # print('\n\n')
    # print(Tika_office2007_PPTX_Parser('/ES/download_test/tmp_ECM_0900bf4b9ef05d6d_0900bf4b9ef05d6d_1608268096033.pptx'))
    # print('\n\n')
    # print(Tika_office2007_PDF_Parser('/ES/download_test/tmp_ECM_0900bf4b985ac045_0900bf4b985ac045_1608370245596.xls'))
    print('\n\n')
    print(Tika_CSV_Parser('/home/ECM_Download/tmp_ECM_0900bf4b9f4c7fbe_0900bf4b9f4c7fbe_1609136631115.csv'))
    # print(Tika_CSV_Parser('/home/ECM_Download/test.csv'))
