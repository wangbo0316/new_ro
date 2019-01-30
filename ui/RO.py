# -*- coding: utf-8 -*-
'''
Created On 18-8-16 下午2:47
    @Author  : WangBo
    @File    : C_Mark.py
    @Software: PyCharm
    @Tag     :
'''
from PyQt5.QtWidgets import QWidget,QGridLayout,QLabel,QPushButton,QFileDialog,QLineEdit
from PyQt5.QtCore import  Qt,pyqtSignal,QThread
import threading
from config.setting import *
from script.RO import upload , calculate

class Job(QThread):
    signal2=pyqtSignal(str,int)

    def p(self,var:str,num:int=1):
        self.signal2.emit(var,num)

    def setFileName(self,var:str):
        self.filename = var

    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True

    def run(self):
        self.p("文件路径读取成功，正在启动解析程序...")
        self.sleep(1)
        self.p("当前文件路径:" + self.filename)
        self.sleep(1)
        upload.UploadRo(self.filename,self)

    def pause(self):
        self.__flag.clear()     # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()

class CalJob(QThread):

    signal=pyqtSignal(str,int)
    dateMonth = ""

    def p(self,var:str,num:int=1):
        self.signal.emit(var,num)


    def __init__(self, *args, **kwargs):
        super(CalJob, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True

    def run(self):
        calculate.Calcullate_RO(self.dateMonth,self)

    def pause(self):
        self.__flag.clear()     # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()


class RO(QWidget):
    fileName = ""
    def __init__(self,*args):
        super(RO, self).__init__(*args)
        self.grid = QGridLayout(self)
        self.grid.addWidget(QLabel(),0,0,1,23)
        self.grid.addWidget(QLabel(), 0, 23, 24, 1)
        self.Excel_Loader()
        self.Mon_Load()
        self.Logo_Print()

    def Excel_Loader(self):
        # ------------title----------------------------------
        self.csv_title = QLabel()
        self.csv_title.setObjectName("title_label")
        self.csv_title.setText('上传Excel文件')
        self.grid.addWidget(self.csv_title, 1,1,1,22, Qt.AlignLeft | Qt.AlignVCenter)
        # ------------lable----------------------------------
        self.csv_lable = QLabel()
        self.csv_lable.setObjectName("normal_label")
        self.csv_lable.setText('请点击右侧按钮选择市场预算表......')
        self.grid.addWidget(self.csv_lable, 3,2,2,19, Qt.AlignLeft | Qt.AlignVCenter)
        # ------------load_btn----------------------------------
        self.csv_btn = QPushButton('...')
        self.csv_btn.setObjectName('load_btn_CSV')
        self.csv_btn.clicked.connect(self.msg)
        self.grid.addWidget(self.csv_btn, 3,21,2,2, Qt.AlignRight | Qt.AlignVCenter)


    def Mon_Load(self):
        # ------------title----------------------------------
        self.mon_title = QLabel()
        self.mon_title.setObjectName("title_label")
        self.mon_title.setText('计算单月数据')
        self.grid.addWidget(self.mon_title, 6, 1, 1, 22, Qt.AlignLeft | Qt.AlignVCenter)
        # ------------input----------------------------------
        self.mon_input = QLineEdit()
        self.mon_input.setObjectName("load_iuput")
        self.mon_input.setPlaceholderText('请输入要装载的月份（如：2018年12月，请输入 2018-12）')
        self.grid.addWidget(self.mon_input, 8, 2, 2, 7, Qt.AlignLeft | Qt.AlignVCenter)
        # ------------load_btn----------------------------------
        self.mon_btn = QPushButton('装载')
        self.mon_btn.setObjectName('load_btn_Mon')
        self.mon_btn.clicked.connect(self.Load_Mon)
        self.grid.addWidget(self.mon_btn, 8, 19, 2, 4, Qt.AlignRight | Qt.AlignVCenter)

    def Load_Mon(self):
        self.thread2 = CalJob()
        self.thread2.signal.connect(self.pL)
        self.thread2.dateMonth = self.mon_input.text()
        self.thread2.start()


    def msg(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self, "选取文件", DEFAULT_OPEN_PATH,
                                                          "All Files (*);;Text Files (*.txt)")
        self.fileName = fileName1
        if fileName1[-5:] == '.xlsx':
            str = fileName1
            if len(str) > 40:
                self.csv_lable.setText(str[0:40] + '......')
            else:
                self.csv_lable.setText(str)
            self.csv_lable.setStyleSheet('#normal_label{color:gray}')
            self.threads = Job()
            self.threads.signal2.connect(self.pL)
            self.threads.setFileName(self.fileName)
            self.threads.start()
        else:
            self.csv_lable.setText('您选择的文件不是xlsx格式，请重新选择......')
            self.csv_lable.setStyleSheet('#normal_label{color:red}')


    def Logo_Print(self):
        # ------------title----------------------------------
        self.logo_label = QLabel()
        self.logo_label.setText('log......')
        self.logo_label.setObjectName("logo_label")
        self.grid.addWidget(self.logo_label, 23, 0, 1, 23, Qt.AlignLeft | Qt.AlignBottom)

    def pL(self,var,num):
        self.logo_label.setText(var)
        if num == 1:
            self.logo_label.setStyleSheet('#logo_label{color:gray}')
        elif num == 2 :
            self.csv_lable.setText(var)
            self.csv_lable.setStyleSheet('#normal_label{color:red}')
            self.logo_label.setStyleSheet('#logo_label{color:red}')
        elif num == 3 :
            self.csv_lable.setText(var)
            self.csv_lable.setStyleSheet('#normal_label{color:#69AAE0}')
            self.logo_label.setStyleSheet('#logo_label{color:#69AAE0}')



