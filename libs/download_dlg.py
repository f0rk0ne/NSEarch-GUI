from PySide6.QtWidgets import QProgressDialog
from PySide6.QtCore import Qt
from PySide6.QtCore import QFile
from PySide6.QtCore import Slot
from PySide6.QtCore import QIODevice
from PySide6.QtCore import QUrl
from PySide6.QtCore import Signal
from PySide6.QtNetwork import QNetworkAccessManager
from PySide6.QtNetwork import QNetworkRequest, QNetworkReply

class DownloadDlg(QProgressDialog):
    
    win, stream = None, None
    finishDownload = Signal(bool, str, name="finishDownload")

    def __init__(self, parent):        
        super(DownloadDlg, self).__init__(parent)
        self.win = parent
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setWindowTitle(
            self.win.i18n.t("setup.database")
        )
        self.setLabelText(
            self.win.i18n.t("setup.downloading")
        )
        self.setRange(0,100)        
        self.init_download()
    
    def init_download(self):
        try:
            self.show()
            netmng = QNetworkAccessManager(self)
            netmng.finished.connect(self.download_dbfinished)   
            netreq = QNetworkRequest()
            netreq.setUrl(QUrl(self.win.utils.db_url))            
            self.netrpl = netmng.get(netreq)
            self.stream = QFile(self.win.utils.db_name)

            if self.stream.open(QIODevice.WriteOnly):                
                self.setValue(1)
                self.netrpl.readyRead.connect(self.start_dbdownload)
                self.netrpl.downloadProgress.connect(self.download_dbprogress)
                self.netrpl.errorOccurred.connect(self.download_dberror)
            else:
                print("error file -> ",self.stream.errorString)            
        except Exception as e:            
            self.win.show_exception(e)        

    def write_data(self):
        try:            
            if self.stream.isOpen():
                self.stream.write(self.netrpl.readAll())
        except Exception as e:
            print(e)

    @Slot()
    def start_dbdownload(self):        
        self.write_data()

    @Slot(int, int)
    def download_dbprogress(self, bytesRecieved, bytesTotal):
        value = bytesRecieved*100/bytesTotal
        self.setValue(value)
        self.write_data()
        
    @Slot()
    def download_dbfinished(self):        
        self.setValue(self.value() + 1)
        self.stream.close()
        self.netrpl.close()
        self.finishDownload.emit(True, None)

    @Slot(str)
    def download_dberror(self, error):        
        if not self.netrpl.isFinished():
            self.stream.remove()
        self.stream.close()
        self.netrpl.close()      
        self.finishDownload.emit(False, error)