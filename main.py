from config import setting
from config import router
from PyQt5.QtWidgets import  QLabel, QPushButton, QVBoxLayout,QListWidget,QStackedWidget,QListWidgetItem,QWidget,QHBoxLayout,QGridLayout,QFileDialog
from PyQt5.QtCore import  QPoint,QSize, Qt
from PyQt5.QtGui import QPixmap

class QTitleLabel(QLabel):
    """
    新建标题栏标签类
    """
    def __init__(self, *args):
        super(QTitleLabel, self).__init__(*args)
        self.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.setFixedHeight(50)

class QTitleButton(QPushButton):
    """
    新建标题栏按钮类
    """

    def __init__(self, *args):
        super(QTitleButton, self).__init__(*args)
        self.setFixedWidth(40)

class QUnFrameWindow(QWidget):
    """
    无边框窗口类
    """
    def __init__(self):
        super(QUnFrameWindow, self).__init__(None, Qt.FramelessWindowHint)  # 设置为顶级窗口，无边框
        self._padding = 5  # 设置边界宽度为5
        self.initTitleLabel()  # 安放标题栏标签
        self.setWindowTitle = self._setTitleText(self.setWindowTitle)  # 用装饰器将设置WindowTitle名字函数共享到标题栏标签上
        self.setWindowTitle("        The LC. Technology Refined Operation Console")
        self.initLayout()  # 设置框架布局
        self.setMinimumWidth(250)
        self.setMouseTracking(True)  # 设置widget鼠标跟踪
        self.initDrag()  # 设置鼠标跟踪判断默认值
        #--------------------------------------------------------
        with open(setting.STATIC_PATH+'\\main.qss', 'r',encoding='UTF-8') as f:  # 导入QListWidget的qss样式
            self.list_style = f.read()

        self.main_layout = QHBoxLayout(self, spacing=0)  # 窗口的整体布局
        self.addLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 50, 0, 0)

        self.left_widget = QListWidget()  # 左侧选项列表
        self.left_widget.setStyleSheet(self.list_style)
        self.main_layout.addWidget(self.left_widget)

        self.right_widget = QStackedWidget()
        self.main_layout.addWidget(self.right_widget)

        self._setup_ui()
        #------------------------------------------------------------------------------------------------------

    def _setup_ui(self):
        '''加载界面ui'''
        self.left_widget.currentRowChanged.connect(self.right_widget.setCurrentIndex)   #list和右侧窗口的index对应绑定
        self.left_widget.setFrameShape(QListWidget.NoFrame)    #去掉边框
        self.left_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  #隐藏滚动条
        self.left_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        for item in router.ROUTER:
            self.item = QListWidgetItem(item, self.left_widget)
            self.item.setSizeHint(QSize(20, 60))
            self.item.setTextAlignment(Qt.AlignCenter)
            self.right_widget.addWidget(router.ROUTER[item]())
            self.right_widget.setObjectName('content')

    def initDrag(self):
        # 设置鼠标跟踪判断扳机默认值
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False

    def initTitleLabel(self):
        # 安放标题栏标签
        self._TitleLabel = QTitleLabel(self)
        self._TitleLabel.setMouseTracking(True)  # 设置标题栏标签鼠标跟踪（如不设，则标题栏内在widget上层，无法实现跟踪）
        self._TitleLabel.setIndent(10)  # 设置标题栏文本缩进
        self._TitleLabel.move(0, 0)  # 标题栏安放到左上角

        self._Ico = QLabel(self._TitleLabel)
        self.setObjectName('title_ico')
        png = QPixmap(setting.STATIC_PATH+'\\main_ico.png')
        self._Ico.setPixmap(png)
        self._Ico.move(10,7)

    def initLayout(self):
        # 设置框架布局
        self._MainLayout = QVBoxLayout()
        self._MainLayout.setSpacing(0)
        # self._MainLayout.addWidget(QLabel(), Qt.AlignLeft)  # 顶一个QLabel在竖放框架第一行，以免正常内容挤占到标题范围里
        # self._MainLayout.addStretch()
        self.setLayout(self._MainLayout)

    def addLayout(self, QLayout):
        # 给widget定义一个addLayout函数，以实现往竖放框架的正确内容区内嵌套Layout框架
        self._MainLayout.addLayout(QLayout)

    def _setTitleText(self, func):
        # 设置标题栏标签的装饰器函数
        def wrapper(*args):
            self._TitleLabel.setText(*args)
            return func(*args)

        return wrapper

    def setTitleAlignment(self, alignment):
        # 给widget定义一个setTitleAlignment函数，以实现标题栏标签的对齐方式设定
        self._TitleLabel.setAlignment(alignment | Qt.AlignVCenter)

    def setCloseButton(self, bool):
        # 给widget定义一个setCloseButton函数，为True时设置一个关闭按钮
        if bool == True:
            self._CloseButton = QTitleButton(b'x'.decode("utf-8"), self)
            self._CloseButton.setObjectName("CloseButton")  # 设置按钮的ObjectName以在qss样式表内定义不同的按钮样式
            self._CloseButton.setMouseTracking(True)  # 设置按钮鼠标跟踪（如不设，则按钮在widget上层，无法实现跟踪）
            self._CloseButton.setFixedHeight(self._TitleLabel.height())  # 设置按钮高度为标题栏高度
            self._CloseButton.clicked.connect(self.close)  # 按钮信号连接到关闭窗口的槽函数

    def setMinMaxButtons(self, bool):
        # 给widget定义一个setMinMaxButtons函数，为True时设置一组最小化最大化按钮
        if bool == True:
            self._MinimumButton = QTitleButton(b'-'.decode("utf-8"), self)
            self._MinimumButton.setObjectName("MinMaxButton")  # 设置按钮的ObjectName以在qss样式表内定义不同的按钮样式
            self._MinimumButton.setMouseTracking(True)  # 设置按钮鼠标跟踪（如不设，则按钮在widget上层，无法实现跟踪）
            self._MinimumButton.setFixedHeight(self._TitleLabel.height())  # 设置按钮高度为标题栏高度
            self._MinimumButton.clicked.connect(self.showMinimized)  # 按钮信号连接到最小化窗口的槽函数

    def resizeEvent(self, QResizeEvent):
        # 自定义窗口调整大小事件
        self._TitleLabel.setFixedWidth(self.width())  # 将标题标签始终设为窗口宽度
        # 分别移动三个按钮到正确的位置
        try:
            self._CloseButton.move(self.width() - self._CloseButton.width(), 0)
        except:
            pass
        try:
            self._MinimumButton.move(self.width() - (self._CloseButton.width() + 1) * 2 + 1, 0)
        except:
            pass
        # 重新调整边界范围以备实现鼠标拖放缩放窗口大小，采用三个列表生成式生成三个列表
        self._right_rect = [QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
                            for y in range(1, self.height() - self._padding)]
        self._bottom_rect = [QPoint(x, y) for x in range(1, self.width() - self._padding)
                             for y in range(self.height() - self._padding, self.height() + 1)]
        self._corner_rect = [QPoint(x, y) for x in range(self.width() - self._padding, self.width() + 1)
                             for y in range(self.height() - self._padding, self.height() + 1)]

    def mousePressEvent(self, event):
        # 重写鼠标点击的事件
        if (event.button() == Qt.LeftButton) and (event.pos() in self._corner_rect):
            # 鼠标左键点击右下角边界区域
            self._corner_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._right_rect):
            # 鼠标左键点击右侧边界区域
            self._right_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._bottom_rect):
            # 鼠标左键点击下侧边界区域
            self._bottom_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.y() < self._TitleLabel.height()):
            # 鼠标左键点击标题栏区域
            self._move_drag = True
            self.move_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        # 判断鼠标位置切换鼠标手势
        if QMouseEvent.pos() in self._corner_rect:
            self.setCursor(Qt.SizeFDiagCursor)
        elif QMouseEvent.pos() in self._bottom_rect:
            self.setCursor(Qt.SizeVerCursor)
        elif QMouseEvent.pos() in self._right_rect:
            self.setCursor(Qt.SizeHorCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        # 当鼠标左键点击不放及满足点击区域的要求后，分别实现不同的窗口调整
        # 没有定义左方和上方相关的5个方向，主要是因为实现起来不难，但是效果很差，拖放的时候窗口闪烁，再研究研究是否有更好的实现
        if Qt.LeftButton and self._right_drag:
            # 右侧调整窗口宽度
            self.resize(QMouseEvent.pos().x(), self.height())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._bottom_drag:
            # 下侧调整窗口高度
            self.resize(self.width(), QMouseEvent.pos().y())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._corner_drag:
            # 右下角同时调整高度和宽度
            self.resize(QMouseEvent.pos().x(), QMouseEvent.pos().y())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._move_drag:
            # 标题栏拖放窗口位置
            self.move(QMouseEvent.globalPos() - self.move_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        # 鼠标释放后，各扳机复位
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    app.setStyleSheet(open(setting.STATIC_PATH+'\\main.qss','r',encoding='UTF-8').read())
    window = QUnFrameWindow()
    window.setCloseButton(True)
    window.setMinMaxButtons(True)
    window.resize(1200,750)
    window.show()
    sys.exit(app.exec_())