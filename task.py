from PyQt5 import QtCore, QtGui, QtWidgets
from task2 import Ui_MainWindow
import sys , os
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
import matplotlib.pyplot 
from matplotlib.animation import FuncAnimation
import pyqtgraph as pg
import time
from PyQt5 import QtCore
import numpy as np
import wave
import pyqtgraph.exporters





class Signal():
    def __init__(self,app,plotArea):
        self.app=app
        self.timer = QtCore.QTimer()
        self.i=0
        self.xss=[]
        self.yss=[]
        self.plotArea=plotArea
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.plot)
        self.filezeft=""
        self.Color="r"
        self.extension=".wav"
       

    def start(self):
        self.timer.start()

    def pause(self):
        self.timer.stop()

    def stop(self):
        self.plotArea.clear()
        self.i=0
        self.timer.stop()

    def browse(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self.app,"QFileDialog.getOpenFileName()", "","All Files ();;Python Files (.py)", options=options)
        self.filezeft=fileName
        ext = os.path.splitext(self.filezeft)[-1].lower()
        if ext==".wav":
            # self.waveopen()
            self.xss=[]
            self.yss=[]
            self.stop()
            if self.filezeft:
                print(self.filezeft)
                spf = wave.open(self.filezeft,'r')
        #Extract Raw Audio from Wav File
                self.yss = spf.readframes(-1)
                self.yss = np.fromstring(self.yss, 'Int16')
                fs = spf.getframerate()
                self.xss=np.linspace(0, len(self.yss)/fs, num=len(self.yss))

    def plot(self):
        self.i=self.i+100
        pen=pg.mkPen(color=self.Color)
        self.plotArea.clear()
        self.plotArea.addLegend()
        self.plotArea.plot(self.xss[0:self.i],self.yss[0:self.i],pen=pen)
        

    def waveopen(self):
        self.xss=[]
        self.yss=[]
        self.stop()
        if self.filezeft:
            print(self.filezeft)
            spf = wave.open(self.filezeft,'r')
        #Extract Raw Audio from Wav File
        self.yss = spf.readframes(-1)
        self.yss = np.fromstring(self.yss, 'Int16')
        fs = spf.getframerate()
        self.xss=np.linspace(0, len(self.yss)/fs, num=len(self.yss))



class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)   
        self.s1=Signal(self,self.ui.widget_2)
        self.ui.Browse.clicked.connect(self.s1.browse)
        self.ui.Start1.clicked.connect(self.s1.start)


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()