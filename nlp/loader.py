from io import StringIO
from io import open
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
import docx

class loader:

    def __init__(self,filename):
        self.filename = filename

    def read_txt(self):
        with open(self.filename, 'r') as f:
            str = f.read()
        return str

    def read_pdf(self):
        with open(self.filename, "rb") as f:
            # resource manager
            rsrcmgr = PDFResourceManager()
            retstr = StringIO()
            laparams = LAParams()
            # device
            device = TextConverter(rsrcmgr, retstr, laparams=laparams)
            process_pdf(rsrcmgr, device, f)
            device.close()
            content = retstr.getvalue()
            retstr.close()
            # 获取所有行
            return str(content)

    def read_word(self):
        d = docx.opendocx(self.filename)
        doc = docx.getdocumenttext(d)
        return str(doc)


# if __name__ == '__main__':

    #测试txt文件
    # file = loader("./file/船代调度工作流程.txt");
    # file.read_txt()

    #测试pdf文件
    # file = loader("./file/船舶安全管理规定.pdf");
    # file.read_pdf()

    #测试word文件
    # file = loader("./file/船舶动力装置概述.docx");
    # file.read_word()
