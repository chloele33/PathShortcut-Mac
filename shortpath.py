# -*- coding: utf-8 -*-
import os,sys,platform, subprocess
from random import randrange
from _codecs import decode
#reload(sys)
#sys.setdefaultencoding('utf8')
# import MySQLdb as ms
# import ConfigParser
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.Qt import *
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QCoreApplication, QPropertyAnimation
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from iconButton import IconButton

class ShortPath(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        self.setFixedSize(QSize(420,700))
        # Create title widgets
        titleWidget=QWidget()
        titleWidget.setObjectName("titleWidget")
        titleWidget.setFixedHeight(45)
#         titleBtn=QPushButton(icon=QIcon("./icons/pathShortcutIcon.png"))
#         titleBtn.setFlat(True)
#         titleBtn.setIconSize(QSize(35, 35))
        titleBtn=QLabel()
        titleBtn.setStyleSheet("image:url('./icons/pathShortcutIcon.png');")
        titleBtn.setFixedSize(QSize(35, 35))
        titleLabel=QLabel("Path Shortcut Tool")
        titleLabel.setFont(QFont("",12,QFont.Bold))
        titleLabel.setStyleSheet("color:rgb(230,231,232)")
        titleSpacer=QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        helpBtn=IconButton('./icons/help.png','./icons/help_hover.png')
        helpBtn.setIconSize(QSize(18,18))
        closeButton=IconButton('./icons/close.png','./icons/close_hover.png')
        closeButton.setIconSize(QSize(18, 18))
        titleLayout=QHBoxLayout()
        titleLayout.addWidget(titleBtn)
        titleLayout.addWidget(titleLabel)
        titleLayout.addItem(titleSpacer)
        titleLayout.addWidget(helpBtn)
        titleLayout.addWidget(closeButton)
        titleLayout.setContentsMargins(6, 0, 8, 0)
        titleWidget.setLayout(titleLayout)
        # Create cent widgets
        self.leftList=QListWidget()
        self.leftList.setObjectName("listWidget")
        self.leftList.setFocusPolicy(Qt.NoFocus)
        self.leftList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.leftList.setDragDropMode(QAbstractItemView.DragDrop)
        self.leftList.setDefaultDropAction(Qt.MoveAction)
        self.rightList=QListWidget()
        self.rightList.setObjectName("listWidget")
        self.rightList.setFocusPolicy(Qt.NoFocus)
        # Create bottom widgets
        self.addBtn=QPushButton("Add Path")
        self.addBtn.setObjectName("nolineBtn")
        self.addBtn.setFixedHeight(28)
        self.removeBtn=QPushButton("Remove Path")
        self.removeBtn.setObjectName("nolineBtn")
        self.removeBtn.setFixedHeight(28)
        self.saveBtn=QPushButton("Save")
        self.saveBtn.setObjectName("nolineBtn")
        self.saveBtn.setFixedHeight(28)
        # Create layouts
        botLayout=QHBoxLayout()
        botLayout.addWidget(self.addBtn)
        botLayout.addWidget(self.removeBtn)
        botLayout.addWidget(self.saveBtn)
        botLayout.setContentsMargins(5, 5, 4, 5)
        botLayout.setSpacing(3)
        centWidget=QMainWindow()
        centSplitter=QSplitter()
        centWidget.setCentralWidget(centSplitter)
        centSplitter.addWidget(self.leftList)
        centSplitter.addWidget(self.rightList)
        centSplitter.setStretchFactor(0,4)
        centSplitter.setStretchFactor(1,2)
        centSplitter.setContentsMargins(5, 5, 6, 0)
        mainLayout=QVBoxLayout()
        mainLayout.addWidget(titleWidget)
        mainLayout.addWidget(centWidget)
        mainLayout.addLayout(botLayout)
        self.setLayout(mainLayout)
        mainLayout.setContentsMargins(0,0,0,0)
        mainLayout.setSpacing(0)
                # Load styleSheet
        qss='''
        QWidget{
            background:rgb(66, 67, 68);}
        QWidget#titleWidget{
            background:rgb(51, 52, 53);}
        QWidget#listWidget{
            background : rgb(56, 57, 58);
            border:none;
            color:rgb(214, 219, 221);}
        QWidget#listWidget::item:hover{
            background : rgb(53, 54, 55);
            color:rgb(232, 232, 232);}
        QWidget#listWidget::item:selected{
            background : rgb(50, 51, 52);
            color:rgb(242, 242, 242);}
        QScrollBar::handle:horizontal{
            background : rgb(60, 61, 62);
            border-radius:6px;
            margin:0 -2px 0 -2px;}
        QScrollBar::handle:vertical{
            background : rgb(60, 61, 62);
            border-radius:6px;
            margin:-2px 0 -2px 0;}
        QScrollBar:add-page:vertical,QScrollBar:sub-page:vertical{ 
            background : rgb(50, 51, 52);}
        QScrollBar:add-page:horizontal,QScrollBar:sub-page:horizontal{
            background : rgb(50, 51, 52);}
        QLabel{
            background:transparent;
            color:rgb(214, 219, 221);}
        QPushButton#nolineBtn{
                background : qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgb(60, 62, 43), stop:1 rgb(40, 42, 44));
                color:rgb(214, 219, 221);
                border:2px groove rgb(40, 42, 44);
                border-radius:10px;
                padding:5px 5px;
                font-size:12px;}    
        QPushButton#nolineBtn:hover{
                color : rgb(208, 208, 100);}
            
        QPushButton#nolineBtn:pressed{
                background : qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgb(40, 42, 44), stop:1 rgb(11, 12, 13));
                padding-top : -1px;}
        '''
        self.setStyleSheet(str(qss))
        # Set functions
        self.defaultFunction()
        helpBtn.clicked.connect(self.helpBtnFunc)
        closeButton.clicked.connect(self.closeButtonFunc)
        self.addBtn.clicked.connect(self.addBtnFunc)
        self.removeBtn.clicked.connect(self.removeBtnFunc)
        self.saveBtn.clicked.connect(self.saveBtnFunc)
        self.leftList.itemClicked.connect(self.itemClickedFunc)
        self.leftList.doubleClicked.connect(self.doubleClickedFunc)
        self.rightList.doubleClicked.connect(self.doubleClickedFunc)
    def helpBtnFunc(self):
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, "help.txt"])
    def addBtnFunc(self):
        currentPath=QFileDialog.getExistingDirectory(directory ="/Users",
                                                     caption="Please select a path",
                                                     options = QFileDialog.ShowDirsOnly)
        curPath=str(currentPath)
        if curPath:self.leftList.addItem(curPath)
    def removeBtnFunc(self):
        selectedItems=self.leftList.selectedItems()
        if not selectedItems:return
        self.rightList.clear()
        for item in selectedItems:
            curRow=self.leftList.row(item)
            curItem=self.leftList.takeItem(curRow)
            self.leftList.removeItemWidget(curItem)
    def saveBtnFunc(self):
        # Get current listItems
        listItems=[]
        for index in range(self.leftList.count()):
            #curPath=str(self.leftList.item(index).text()).decode('utf-8','ignore')
            curPath=str(self.leftList.item(index).text())
            if curPath:listItems.append(curPath+"\n")
        _, cury, _, _ = self.geometry().getCoords()
        listItems.append(str(cury))
        with open("pathes.txt","w") as pathFile:
            pathFile.writelines(listItems)
    def itemClickedFunc(self):
        selectedItems=self.leftList.selectedItems()
        if not selectedItems:return
        curItem=str(selectedItems[0].text())
        self.rightList.clear()
        fileList=os.listdir(curItem)
        if not fileList:return
        fileList.sort()
        self.rightList.addItems(fileList)
    def doubleClickedFunc(self):
        selectedItems=self.rightList.selectedItems()
        if not selectedItems:
            selectedItems=self.leftList.selectedItems()
            if not selectedItems:return
            #curItem=str(selectedItems[0].text()).decode('utf-8','ignore')
            curItem=str(selectedItems[0].text())
            #os.open(curItem)
            opener ="open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, curItem])
        else:
            leftItem=str(self.leftList.selectedItems()[0].text())
            rightItem=str(selectedItems[0].text())
            tarItem=leftItem+"/"+rightItem
            #os.open(tarItem)
            opener ="open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, tarItem])
    def posObjs(self):
        screen = QDesktopWidget().screenGeometry()
        self.screenWidth=screen.width()
        self.screenHeight=screen.height()
        size =  self.geometry()
        self.winWidth=size.width()
        self.winHeight=size.height()
        self.x, self.y, _, _ = size.getCoords()
        self.cursorx=QCursor.pos().x()
        self.cursory=QCursor.pos().y()
    def defaultFunction(self):
        if os.path.exists("pathes.txt"):
            with open("pathes.txt","r") as pathFile:
                pathlist=pathFile.readlines()
                if pathlist:
                    #self.initpathes=[item.decode('utf-8','ignore')[:-1] for item in pathlist[:-1]]
                    self.initpathes=[item[:-1] for item in pathlist[:-1]]
                    self.leftList.addItems(self.initpathes)
                    verx=pathlist[-1]
                else:
                    self.initpathes=[]
                    verx=""
        else:
            self.initpathes=[]
            verx=""
        if verx:
            self.move(0, int(verx))
        else:
            screenHeight=QDesktopWidget().screenGeometry().height()
            winHeight=self.geometry().height()
            self.move(0, (screenHeight-winHeight)/2)
    def enterEvent(self,event):
        self.posObjs()
        if self.cursorx<6:
            self.winOut(0.3,1.0,320,-412,420)
    def leaveEvent(self,event):
        self.posObjs()
        if self.x <= 0:
            self.winIn(1.0,0.3,320,-412)
    def winOut(self,startOpacity,endOpacity,aniTime,startPos,widgetWidth):
        tempArray = QByteArray()
        tempArray.append("windowOpacity")
        opacity_anim = QPropertyAnimation(self, tempArray)
        opacity_anim.setStartValue(startOpacity)
        opacity_anim.setEndValue(endOpacity)
        opacity_anim.setDuration(aniTime)
        opacity_anim_curve = QEasingCurve()
        opacity_anim_curve.setType(QEasingCurve.OutQuad)
        opacity_anim.setEasingCurve(opacity_anim_curve)
 
        tempArray2 = QByteArray()
        tempArray2.append("geometry")
        size_anim = QPropertyAnimation(self, tempArray2)
        size_start = QRect(startPos, self.y, 0, self.winHeight)
        size_end   = QRect(0, self.y, widgetWidth, self.winHeight)
        size_anim.setStartValue(size_start)
        size_anim.setEndValue(size_end)
        size_anim.setDuration(aniTime)
        size_anim_curve = QEasingCurve()
        size_anim_curve.setType(QEasingCurve.OutQuad)
        size_anim.setEasingCurve(size_anim_curve)
        
        opacity_anim.start(QAbstractAnimation.DeleteWhenStopped)
        size_anim.start(QAbstractAnimation.DeleteWhenStopped)
        
        self._animation = QSequentialAnimationGroup()
        self.setWindowOpacity(startOpacity)
        self._animation.addAnimation(opacity_anim)
        self._animation.addAnimation(size_anim)
        self._animation.finished.connect(self._animation.clear)
    def winIn(self,startOpacity,endOpacity,aniTime,endPos):
        tempArray=QByteArray()
        tempArray.append("windowOpacity")
        opacity_anim = QPropertyAnimation(self, tempArray)
        opacity_anim.setStartValue(startOpacity)
        opacity_anim.setEndValue(endOpacity)
        opacity_anim.setDuration(aniTime)
        opacity_anim_curve = QEasingCurve()
        opacity_anim_curve.setType(QEasingCurve.OutQuad)
        opacity_anim.setEasingCurve(opacity_anim_curve)

        tempArray2=QByteArray()
        tempArray2.append("geometry")
        size_anim = QPropertyAnimation(self, tempArray2)
        size_start = QRect(self.x, self.y, self.winWidth, self.winHeight)
        size_end   = QRect(endPos, self.y, self.winWidth, self.winHeight)
        size_anim.setStartValue(size_start)
        size_anim.setEndValue(size_end)
        size_anim.setDuration(aniTime)      
        size_anim_curve = QEasingCurve()
        size_anim_curve.setType(QEasingCurve.OutQuad)
        size_anim.setEasingCurve(size_anim_curve)
        
        opacity_anim.start(QAbstractAnimation.DeleteWhenStopped)
        size_anim.start(QAbstractAnimation.DeleteWhenStopped)

        self._animation = QSequentialAnimationGroup()
        self.setWindowOpacity(startOpacity)
        self._animation.addAnimation(opacity_anim)
        self._animation.addAnimation(size_anim)
        self._animation.finished.connect(self._animation.clear)
    def mousePressEvent(self,event):
        if event.button()==Qt.LeftButton:
            self.dragPosition=event.globalPos()-self.frameGeometry().topLeft()
            event.accept()
    def mouseMoveEvent(self,event):
        if event.buttons()==Qt.LeftButton: 
            self.move(event.globalPos()-self.dragPosition)
            self.posObjs()
            if self.y<0:
                self.move(self.x,0)
            event.accept()
    def keyPressEvent(self,event):
        if event.key()==Qt.Key_Escape:
            self.closeButtonFunc()
    def closeButtonFunc(self):
        tempArray=QByteArray()
        tempArray.append("windowOpacity")
        opacity_anim = QPropertyAnimation(self, tempArray)
        #opacity_anim.setTargetObject()
        opacity_anim.setStartValue(1.0)
        opacity_anim.setEndValue(0.0)
        opacity_anim.setDuration(620)
        opacity_anim_curve = QEasingCurve()
        opacity_anim_curve.setType(QEasingCurve.OutQuad)
        opacity_anim.setEasingCurve(opacity_anim_curve)
        
        size =  self.geometry()
        self.winWidth=size.width()
        self.winHeight=size.height()
        self.x, self.y, _, _ = size.getCoords()
        
        tempArray2=QByteArray()
        tempArray2.append("geometry")
        size_anim = QPropertyAnimation(self, tempArray2)
        size_start = QRect(self.x, self.y, self.winWidth, self.winHeight)
        size_end   = QRect(self.x, self.y, 0, self.winHeight)
        size_anim.setStartValue(size_start)
        size_anim.setEndValue(size_end)
        size_anim.setDuration(620)      
        size_anim_curve = QEasingCurve()
        size_anim_curve.setType(QEasingCurve.OutQuad)
        size_anim.setEasingCurve(size_anim_curve)
        
        size_anim.start(QAbstractAnimation.DeleteWhenStopped)
        opacity_anim.start(QAbstractAnimation.DeleteWhenStopped)
    
        self._animation = QSequentialAnimationGroup()
        self._animation.addAnimation(opacity_anim)
        self._animation.addAnimation(size_anim)
        self._animation.finished.connect(self._animation.clear)
        self.setWindowOpacity(1.0)
        QTimer.singleShot(620, self.close)
        
if __name__ == "__main__":
    app=QApplication(sys.argv)
    shortPath=ShortPath()
    shortPath.show()
    sys.exit(app.exec_())

    