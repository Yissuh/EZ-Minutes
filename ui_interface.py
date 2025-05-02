# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interface.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QFrame, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QMainWindow,
    QPushButton, QSizePolicy, QStackedWidget, QTextEdit,
    QVBoxLayout, QWidget)
import images_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.WindowModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(994, 593)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(651, 466))
        MainWindow.setMaximumSize(QSize(2122, 1108))
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"QFrame#centralwidget {\n"
"    border-image: url(:/bgs/images/ht3.png) 50 25 50 25 stretch stretch;\n"
"}\n"
"")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.sideMenuContainer = QFrame(self.centralwidget)
        self.sideMenuContainer.setObjectName(u"sideMenuContainer")
        self.sideMenuContainer.setMinimumSize(QSize(200, 0))
        self.sideMenuContainer.setMaximumSize(QSize(0, 16777215))
        self.sideMenuContainer.setFrameShape(QFrame.NoFrame)
        self.sideMenuContainer.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.sideMenuContainer)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.sideMenu = QFrame(self.sideMenuContainer)
        self.sideMenu.setObjectName(u"sideMenu")
        self.sideMenu.setMinimumSize(QSize(196, 0))
        self.sideMenu.setStyleSheet(u"background-color: rgb(78, 64, 50)\n"
"")
        self.sideMenu.setFrameShape(QFrame.StyledPanel)
        self.sideMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.sideMenu)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.sideMenu)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 11, 0, 0)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setPixmap(QPixmap(u":/icons/images/icons/LogoUpdate.png"))
        self.label.setScaledContents(False)
        self.label.setMargin(-2)

        self.verticalLayout_4.addWidget(self.label, 0, Qt.AlignHCenter|Qt.AlignTop)


        self.verticalLayout_3.addWidget(self.frame, 0, Qt.AlignTop)

        self.frame_5 = QFrame(self.sideMenu)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy1)
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_5)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_7 = QFrame(self.frame_5)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_7)
        self.verticalLayout_6.setSpacing(10)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 20, 0, 70)
        self.homeButton = QPushButton(self.frame_7)
        self.homeButton.setObjectName(u"homeButton")
        self.homeButton.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(78, 64, 50)\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:  rgb(167, 141, 120) \n"
"}\n"
"")
        self.homeButton.setCursor(Qt.PointingHandCursor)
        icon = QIcon()
        icon.addFile(u":/buttons/images/buttons/Home.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.homeButton.setIcon(icon)
        self.homeButton.setIconSize(QSize(50, 24))
        self.homeButton.setFlat(True)

        self.verticalLayout_6.addWidget(self.homeButton)

        self.LogButton = QPushButton(self.frame_7)
        self.LogButton.setObjectName(u"LogButton")
        self.LogButton.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(78, 64, 50)\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:  rgb(167, 141, 120) \n"
"}\n"
"")
        self.LogButton.setCursor(Qt.PointingHandCursor)
        icon1 = QIcon()
        icon1.addFile(u":/buttons/images/buttons/ActivityLog.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.LogButton.setIcon(icon1)
        self.LogButton.setIconSize(QSize(80, 24))
        self.LogButton.setFlat(True)

        self.verticalLayout_6.addWidget(self.LogButton)


        self.verticalLayout_5.addWidget(self.frame_7, 0, Qt.AlignTop)

        self.frame_8 = QFrame(self.frame_5)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Raised)

        self.verticalLayout_5.addWidget(self.frame_8)

        self.frame_9 = QFrame(self.frame_5)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Raised)

        self.verticalLayout_5.addWidget(self.frame_9)


        self.verticalLayout_3.addWidget(self.frame_5)

        self.frame_6 = QFrame(self.sideMenu)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_3.addWidget(self.frame_6, 0, Qt.AlignBottom)


        self.verticalLayout_2.addWidget(self.sideMenu)


        self.horizontalLayout.addWidget(self.sideMenuContainer)

        self.mainBody = QFrame(self.centralwidget)
        self.mainBody.setObjectName(u"mainBody")
        self.mainBody.setStyleSheet(u"QFrame#mainBody {\n"
"    border-image: url(:/bgs/images/ht3.png) 50 25 50 25 stretch stretch;\n"
"}\n"
"")
        self.mainBody.setFrameShape(QFrame.StyledPanel)
        self.mainBody.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.mainBody)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.header = QFrame(self.mainBody)
        self.header.setObjectName(u"header")
        self.header.setStyleSheet(u"background-color: rgb(78, 64, 50)\n"
"")
        self.header.setFrameShape(QFrame.NoFrame)
        self.header.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.header)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.header)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.sideDrawerButton = QPushButton(self.frame_3)
        self.sideDrawerButton.setObjectName(u"sideDrawerButton")
        self.sideDrawerButton.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(78, 64, 50)\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:  rgb(167, 141, 120) \n"
"}\n"
"")
        self.sideDrawerButton.setCursor(Qt.PointingHandCursor)
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/icons/openDrawer.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.sideDrawerButton.setIcon(icon2)
        self.sideDrawerButton.setIconSize(QSize(24, 16))
        self.sideDrawerButton.setFlat(True)

        self.horizontalLayout_4.addWidget(self.sideDrawerButton)


        self.horizontalLayout_2.addWidget(self.frame_3, 0, Qt.AlignLeft)

        self.frame_4 = QFrame(self.header)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_2.addWidget(self.frame_4)

        self.frame_2 = QFrame(self.header)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.minimizeWindow = QPushButton(self.frame_2)
        self.minimizeWindow.setObjectName(u"minimizeWindow")
        self.minimizeWindow.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(78, 64, 50)\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:  rgb(167, 141, 120) \n"
"}\n"
"")
        icon3 = QIcon()
        icon3.addFile(u":/icons/images/icons/minimize.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.minimizeWindow.setIcon(icon3)
        self.minimizeWindow.setIconSize(QSize(16, 16))
        self.minimizeWindow.setFlat(True)

        self.horizontalLayout_3.addWidget(self.minimizeWindow)

        self.maximizeWindow = QPushButton(self.frame_2)
        self.maximizeWindow.setObjectName(u"maximizeWindow")
        self.maximizeWindow.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(78, 64, 50)\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:  rgb(167, 141, 120) \n"
"}\n"
"")
        icon4 = QIcon()
        icon4.addFile(u":/icons/images/icons/maxWindow.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.maximizeWindow.setIcon(icon4)
        self.maximizeWindow.setIconSize(QSize(16, 16))
        self.maximizeWindow.setFlat(True)

        self.horizontalLayout_3.addWidget(self.maximizeWindow)

        self.close = QPushButton(self.frame_2)
        self.close.setObjectName(u"close")
        self.close.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(78, 64, 50)\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:  rgb(167, 141, 120) \n"
"}\n"
"")
        icon5 = QIcon()
        icon5.addFile(u":/icons/images/icons/close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.close.setIcon(icon5)
        self.close.setIconSize(QSize(16, 16))
        self.close.setFlat(True)

        self.horizontalLayout_3.addWidget(self.close)


        self.horizontalLayout_2.addWidget(self.frame_2, 0, Qt.AlignRight)


        self.verticalLayout.addWidget(self.header, 0, Qt.AlignTop)

        self.mainBodyContent = QFrame(self.mainBody)
        self.mainBodyContent.setObjectName(u"mainBodyContent")
        sizePolicy1.setHeightForWidth(self.mainBodyContent.sizePolicy().hasHeightForWidth())
        self.mainBodyContent.setSizePolicy(sizePolicy1)
        self.mainBodyContent.setStyleSheet(u"QFrame#mainBodyContent {\n"
"    border-image: url(:/bgs/images/ht3.png) 50 25 50 25 stretch stretch;\n"
"}\n"
"")
        self.mainBodyContent.setFrameShape(QFrame.NoFrame)
        self.mainBodyContent.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.mainBodyContent)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.mainBodyContent)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setAutoFillBackground(False)
        self.stackedWidget.setStyleSheet(u"")
        self.GeneratePage2 = QWidget()
        self.GeneratePage2.setObjectName(u"GeneratePage2")
        self.verticalLayout_8 = QVBoxLayout(self.GeneratePage2)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.frame_10 = QFrame(self.GeneratePage2)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setStyleSheet(u"background-color:rgb(255, 255, 255)")
        self.frame_10.setFrameShape(QFrame.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.frame_10.setLineWidth(0)
        self.verticalLayout_9 = QVBoxLayout(self.frame_10)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(20, 20, 20, 5)
        self.frame_13 = QFrame(self.frame_10)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.NoFrame)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.verticalLayout_19 = QVBoxLayout(self.frame_13)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.minutesDisplay = QTextEdit(self.frame_13)
        self.minutesDisplay.setObjectName(u"minutesDisplay")
        self.minutesDisplay.setStyleSheet(u"QTextEdit {\n"
"    font-family: \"Courier New\";\n"
"    font-size: 10pt;\n"
"    color: #54493E;\n"
"}\n"
"\n"
"")
        self.minutesDisplay.setFrameShape(QFrame.Box)
        self.minutesDisplay.setLineWidth(3)
        self.minutesDisplay.setLineWrapColumnOrWidth(50)

        self.verticalLayout_19.addWidget(self.minutesDisplay)

        self.replaceTextBtn = QPushButton(self.frame_13)
        self.replaceTextBtn.setObjectName(u"replaceTextBtn")
        self.replaceTextBtn.setStyleSheet(u"QPushButton {\n"
"    font-family: \"Times New Roman\";\n"
"    font-size: 9pt;\n"
"    color: #54493E;\n"
"    text-decoration: underline;\n"
"}\n"
"QPushButton:hover {\n"
"    color: #7A6C5B;  /* example hover color: lighter shade */\n"
"}\n"
"")
        self.replaceTextBtn.setCursor(Qt.PointingHandCursor)
        self.replaceTextBtn.setFlat(True)

        self.verticalLayout_19.addWidget(self.replaceTextBtn, 0, Qt.AlignLeft)


        self.verticalLayout_9.addWidget(self.frame_13)

        self.frame_12 = QFrame(self.frame_10)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.NoFrame)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, -1, -1, 60)
        self.frame_14 = QFrame(self.frame_12)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.NoFrame)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.returnBtn = QPushButton(self.frame_14)
        self.returnBtn.setObjectName(u"returnBtn")
        self.returnBtn.setMinimumSize(QSize(80, 30))
        self.returnBtn.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(78, 64, 50)\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:  rgb(185, 128, 118)\n"
"}\n"
"")     
        self.returnBtn.setCursor(Qt.PointingHandCursor)
        icon6 = QIcon()
        icon6.addFile(u":/buttons/images/buttons/returnBtn.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.returnBtn.setIcon(icon6)
        self.returnBtn.setIconSize(QSize(60, 16))
        self.returnBtn.setFlat(True)

        self.horizontalLayout_5.addWidget(self.returnBtn)

        self.generateBtn = QPushButton(self.frame_14)
        self.generateBtn.setObjectName(u"generateBtn")
        self.generateBtn.setMinimumSize(QSize(100, 30))
        self.generateBtn.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(78, 64, 50)\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:  rgb(167, 141, 120) \n"
"}\n"
"")
        self.generateBtn.setCursor(Qt.PointingHandCursor)
        icon7 = QIcon()
        icon7.addFile(u":/buttons/images/buttons/generateBtn.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.generateBtn.setIcon(icon7)
        self.generateBtn.setIconSize(QSize(70, 20))
        self.generateBtn.setFlat(True)

        self.horizontalLayout_5.addWidget(self.generateBtn)


        self.horizontalLayout_7.addWidget(self.frame_14, 0, Qt.AlignLeft)

        self.frame_15 = QFrame(self.frame_12)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setFrameShape(QFrame.NoFrame)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.saveBtn = QPushButton(self.frame_15)
        self.saveBtn.setObjectName(u"saveBtn")
        self.saveBtn.setMinimumSize(QSize(70, 30))
        self.saveBtn.setStyleSheet(u"QPushButton {\n"
"    background-color:rgb(78, 64, 50)\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:rgb(185, 186, 143)\n"
"}")
        self.saveBtn.setCursor(Qt.PointingHandCursor)
        icon8 = QIcon()
        icon8.addFile(u":/buttons/images/buttons/saveBtn.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.saveBtn.setIcon(icon8)
        self.saveBtn.setIconSize(QSize(50, 18))
        self.saveBtn.setFlat(True)

        self.horizontalLayout_8.addWidget(self.saveBtn)


        self.horizontalLayout_7.addWidget(self.frame_15, 0, Qt.AlignRight)


        self.verticalLayout_9.addWidget(self.frame_12)


        self.verticalLayout_8.addWidget(self.frame_10)

        self.stackedWidget.addWidget(self.GeneratePage2)
        self.GeneratePage1 = QWidget()
        self.GeneratePage1.setObjectName(u"GeneratePage1")
        self.verticalLayout_12 = QVBoxLayout(self.GeneratePage1)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.frame_16 = QFrame(self.GeneratePage1)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setStyleSheet(u"background-color:rgb(255, 255, 255)")
        self.frame_16.setFrameShape(QFrame.NoFrame)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.frame_16)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.frame_20 = QFrame(self.frame_16)
        self.frame_20.setObjectName(u"frame_20")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame_20.sizePolicy().hasHeightForWidth())
        self.frame_20.setSizePolicy(sizePolicy2)
        self.frame_20.setMaximumSize(QSize(16777215, 100))
        self.frame_20.setFrameShape(QFrame.NoFrame)
        self.frame_20.setFrameShadow(QFrame.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.frame_20)
        self.verticalLayout_15.setSpacing(15)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.clearBtn = QPushButton(self.frame_20)
        self.clearBtn.setObjectName(u"clearBtn")
        self.clearBtn.setStyleSheet(u"QPushButton:hover {\n"
"    background-color: rgb(185, 128, 118);\n"
"\n"
"}")
        icon9 = QIcon()
        icon9.addFile(u":/icons/images/icons/closeTwo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.clearBtn.setIcon(icon9)
        self.clearBtn.setIconSize(QSize(16, 16))
        self.clearBtn.setFlat(True)

        self.verticalLayout_15.addWidget(self.clearBtn, 0, Qt.AlignLeft)

        self.agendaInput = QTextEdit(self.frame_20)
        self.agendaInput.setObjectName(u"agendaInput")
        self.agendaInput.setMaximumSize(QSize(16777215, 16777215))
        self.agendaInput.setStyleSheet(u"QTextEdit {\n"
"    font-family: \"Courier New\";\n"
"    font-size: 10pt;\n"
"    color: #54493E;\n"
"}\n"
"\n"
"")
        self.agendaInput.setFrameShape(QFrame.Box)
        self.agendaInput.setLineWidth(3)

        self.verticalLayout_15.addWidget(self.agendaInput)


        self.verticalLayout_13.addWidget(self.frame_20)

        self.frame_17 = QFrame(self.frame_16)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setMaximumSize(QSize(16777215, 80))
        self.frame_17.setFrameShape(QFrame.NoFrame)
        self.frame_17.setFrameShadow(QFrame.Sunken)
        self.frame_17.setLineWidth(2)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_17)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.attendeesInput = QTextEdit(self.frame_17)
        self.attendeesInput.setObjectName(u"attendeesInput")
        self.attendeesInput.setStyleSheet(u"QTextEdit {\n"
"    font-family: \"Courier New\";\n"
"    font-size: 10pt;\n"
"    color: #54493E;\n"
"}\n"
"\n"
"")
        self.attendeesInput.setFrameShape(QFrame.Box)
        self.attendeesInput.setLineWidth(3)

        self.horizontalLayout_11.addWidget(self.attendeesInput)


        self.verticalLayout_13.addWidget(self.frame_17)

        self.display = QFrame(self.frame_16)
        self.display.setObjectName(u"display")
        sizePolicy1.setHeightForWidth(self.display.sizePolicy().hasHeightForWidth())
        self.display.setSizePolicy(sizePolicy1)
        self.display.setFrameShape(QFrame.NoFrame)
        self.display.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.display)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.transcriptFrame = QFrame(self.display)
        self.transcriptFrame.setObjectName(u"transcriptFrame")
        sizePolicy1.setHeightForWidth(self.transcriptFrame.sizePolicy().hasHeightForWidth())
        self.transcriptFrame.setSizePolicy(sizePolicy1)
        self.transcriptFrame.setFrameShape(QFrame.NoFrame)
        self.transcriptFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.transcriptFrame)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, -1, 0, -1)
        self.transcriptDisplay = QTextEdit(self.transcriptFrame)
        self.transcriptDisplay.setObjectName(u"transcriptDisplay")
        self.transcriptDisplay.setMinimumSize(QSize(0, 170))
        self.transcriptDisplay.setMaximumSize(QSize(16777215, 1000))
        self.transcriptDisplay.setStyleSheet(u"QTextEdit {\n"
"    font-family: \"Courier New\";\n"
"    font-size: 10pt;\n"
"    color: #54493E;\n"
"}\n"
"\n"
"")
        self.transcriptDisplay.setFrameShape(QFrame.Box)
        self.transcriptDisplay.setLineWidth(3)
        self.transcriptDisplay.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.transcriptDisplay.setLineWrapColumnOrWidth(50)

        self.horizontalLayout_17.addWidget(self.transcriptDisplay)


        self.verticalLayout_14.addWidget(self.transcriptFrame)

        self.speakerFrame = QFrame(self.display)
        self.speakerFrame.setObjectName(u"speakerFrame")
        self.speakerFrame.setMinimumSize(QSize(0, 20))
        self.speakerFrame.setMaximumSize(QSize(16777215, 60))
        self.speakerFrame.setFrameShape(QFrame.NoFrame)
        self.speakerFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.speakerFrame)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(40, 0, 40, -1)
        self.label_2 = QLabel(self.speakerFrame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"QLabel {\n"
"    font-family: \"Courier New\";\n"
"    font-size: 8pt;\n"
"    color: #54493E;\n"
"}\n"
"\n"
"")

        self.horizontalLayout_16.addWidget(self.label_2)

        self.speakerNumber = QTextEdit(self.speakerFrame)
        self.speakerNumber.setObjectName(u"speakerNumber")
        self.speakerNumber.setStyleSheet(u"QTextEdit {\n"
"    font-family: \"Courier New\";\n"
"    font-size: 10pt;\n"
"    color: #54493E;\n"
"}\n"
"\n"
"")
        self.speakerNumber.setFrameShape(QFrame.Box)
        self.speakerNumber.setLineWidth(2)

        self.horizontalLayout_16.addWidget(self.speakerNumber)

        self.label_3 = QLabel(self.speakerFrame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"QLabel {\n"
"    font-family: \"Courier New\";\n"
"    font-size: 8pt;\n"
"    color: #54493E;\n"
"}\n"
"\n"
"")

        self.horizontalLayout_16.addWidget(self.label_3)

        self.speakerName = QTextEdit(self.speakerFrame)
        self.speakerName.setObjectName(u"speakerName")
        self.speakerName.setStyleSheet(u"QTextEdit {\n"
"    font-family: \"Courier New\";\n"
"    font-size: 10pt;\n"
"    color: #54493E;\n"
"}\n"
"\n"
"")
        self.speakerName.setFrameShape(QFrame.Box)
        self.speakerName.setLineWidth(2)

        self.horizontalLayout_16.addWidget(self.speakerName)

        self.assignSpeakerBtn = QPushButton(self.speakerFrame)
        self.assignSpeakerBtn.setObjectName(u"assignSpeakerBtn")
        self.assignSpeakerBtn.setStyleSheet(u"QPushButton {\n"
"    font-family: \"Courier New\";\n"
"    font-size: 10pt;\n"
"    color: rgb(41, 28, 14);\n"
"    background-color: rgb(225, 212, 194);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:  rgb(167, 141, 120) \n"
"}\n"
"")
        self.assignSpeakerBtn.setCursor(Qt.PointingHandCursor)
        self.assignSpeakerBtn.setFlat(True)

        self.horizontalLayout_16.addWidget(self.assignSpeakerBtn)


        self.verticalLayout_14.addWidget(self.speakerFrame)

        self.uploadedFileLabel = QLabel(self.display)
        self.uploadedFileLabel.setObjectName(u"uploadedFileLabel")
        self.uploadedFileLabel.setStyleSheet(u"color: rgb(185, 186, 143)")
        self.uploadedFileLabel.setIndent(-1)

        self.verticalLayout_14.addWidget(self.uploadedFileLabel)


        self.verticalLayout_13.addWidget(self.display)

        self.buttonsFrame = QFrame(self.frame_16)
        self.buttonsFrame.setObjectName(u"buttonsFrame")
        self.buttonsFrame.setMinimumSize(QSize(0, 80))
        self.buttonsFrame.setFrameShape(QFrame.NoFrame)
        self.buttonsFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.buttonsFrame)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(-1, 0, -1, 15)
        self.frame_21 = QFrame(self.buttonsFrame)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setFrameShape(QFrame.NoFrame)
        self.frame_21.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_21)
        self.horizontalLayout_14.setSpacing(6)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 30)
        self.uploadBtn = QPushButton(self.frame_21)
        self.uploadBtn.setObjectName(u"uploadBtn")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.uploadBtn.sizePolicy().hasHeightForWidth())
        self.uploadBtn.setSizePolicy(sizePolicy3)
        self.uploadBtn.setMinimumSize(QSize(70, 0))
        self.uploadBtn.setMaximumSize(QSize(30, 30))
        self.uploadBtn.setStyleSheet(u"QPushButton {\n"
"    background-color:rgb(78, 64, 50)\n"
"}\n"
"\n"
"\n"
"QPushButton:hover {\n"
"    background-color:  rgb(167, 141, 120) \n"
"}")
        self.uploadBtn.setCursor(Qt.PointingHandCursor)
        icon10 = QIcon()
        icon10.addFile(u":/buttons/images/buttons/uploadBtn.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.uploadBtn.setIcon(icon10)
        self.uploadBtn.setIconSize(QSize(55, 18))
        self.uploadBtn.setFlat(True)

        self.horizontalLayout_14.addWidget(self.uploadBtn)

        self.transcribeBtn = QPushButton(self.frame_21)
        self.transcribeBtn.setObjectName(u"transcribeBtn")
        self.transcribeBtn.setMinimumSize(QSize(100, 0))
        self.transcribeBtn.setMaximumSize(QSize(150, 30))
        self.transcribeBtn.setStyleSheet(u"QPushButton {\n"
"    background-color:rgb(78, 64, 50)\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:  rgb(167, 141, 120) \n"
"}\n"
"")
        self.transcribeBtn.setCursor(Qt.PointingHandCursor)
        icon11 = QIcon()
        icon11.addFile(u":/buttons/images/buttons/transcribeBtn.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.transcribeBtn.setIcon(icon11)
        self.transcribeBtn.setIconSize(QSize(70, 20))
        self.transcribeBtn.setFlat(True)

        self.horizontalLayout_14.addWidget(self.transcribeBtn)


        self.horizontalLayout_13.addWidget(self.frame_21, 0, Qt.AlignLeft|Qt.AlignTop)

        self.frame_22 = QFrame(self.buttonsFrame)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setFrameShape(QFrame.NoFrame)
        self.frame_22.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_22)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(150, 0, 0, 30)
        self.proceedBtn = QPushButton(self.frame_22)
        self.proceedBtn.setObjectName(u"proceedBtn")
        self.proceedBtn.setMinimumSize(QSize(80, 0))
        self.proceedBtn.setMaximumSize(QSize(120, 30))
        self.proceedBtn.setStyleSheet(u"QPushButton {\n"
"    background-color:rgb(78, 64, 50)\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:rgb(185, 186, 143)\n"
"}")
        icon12 = QIcon()
        icon12.addFile(u":/buttons/images/buttons/proceedBtn.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.proceedBtn.setIcon(icon12)
        self.proceedBtn.setIconSize(QSize(60, 20))
        self.proceedBtn.setFlat(True)

        self.horizontalLayout_15.addWidget(self.proceedBtn)


        self.horizontalLayout_13.addWidget(self.frame_22, 0, Qt.AlignRight|Qt.AlignTop)


        self.verticalLayout_13.addWidget(self.buttonsFrame)


        self.verticalLayout_12.addWidget(self.frame_16)

        self.stackedWidget.addWidget(self.GeneratePage1)
        self.HomePage = QWidget()
        self.HomePage.setObjectName(u"HomePage")
        self.HomePage.setStyleSheet(u"background-color:rgb(225, 212, 194)")
        self.verticalLayout_10 = QVBoxLayout(self.HomePage)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.backgroundFrame = QFrame(self.HomePage)
        self.backgroundFrame.setObjectName(u"backgroundFrame")
        self.backgroundFrame.setAutoFillBackground(False)
        self.backgroundFrame.setStyleSheet(u"QFrame#backgroundFrame {\n"
"    border-image: url(:/bgs/images/homebg.png) 50 25 0 25 stretch stretch;\n"
"}\n"
"")
        self.backgroundFrame.setFrameShape(QFrame.NoFrame)
        self.backgroundFrame.setFrameShadow(QFrame.Raised)
        self.backgroundFrame.setLineWidth(0)
        self.backgroundFrame.setMidLineWidth(0)
        self.verticalLayout_11 = QVBoxLayout(self.backgroundFrame)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.frame_23 = QFrame(self.backgroundFrame)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setStyleSheet(u"QFrame {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}\n"
"")
        self.frame_23.setFrameShape(QFrame.StyledPanel)
        self.frame_23.setFrameShadow(QFrame.Raised)

        self.verticalLayout_11.addWidget(self.frame_23)

        self.origFrame = QFrame(self.backgroundFrame)
        self.origFrame.setObjectName(u"origFrame")
        self.origFrame.setStyleSheet(u"QFrame {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}\n"
"")
        self.origFrame.setFrameShape(QFrame.StyledPanel)
        self.origFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.origFrame)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.topframe = QFrame(self.origFrame)
        self.topframe.setObjectName(u"topframe")
        self.topframe.setFrameShape(QFrame.StyledPanel)
        self.topframe.setFrameShadow(QFrame.Raised)
        self.verticalLayout_17 = QVBoxLayout(self.topframe)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 15)
        self.getStartedBtn = QPushButton(self.topframe)
        self.getStartedBtn.setObjectName(u"getStartedBtn")
        self.getStartedBtn.setMinimumSize(QSize(180, 40))
        self.getStartedBtn.setMaximumSize(QSize(16777215, 16777215))
        self.getStartedBtn.setStyleSheet(u"QPushButton {\n"
"    background-color: #B9A493;   /* fill color */\n"
"    color: #E7DDCE;\n"
"    border: 2px solid #54493E;   /* stroke line */\n"
"    border-radius: 15px;         /* rounder corners */\n"
"    \n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #CBB8A5;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #A8937D;\n"
"}\n"
"")
        self.getStartedBtn.setCursor(Qt.PointingHandCursor)
        icon13 = QIcon()
        icon13.addFile(u":/buttons/images/buttons/getStartedBtn.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.getStartedBtn.setIcon(icon13)
        self.getStartedBtn.setIconSize(QSize(100, 16))

        self.verticalLayout_17.addWidget(self.getStartedBtn)


        self.verticalLayout_16.addWidget(self.topframe, 0, Qt.AlignHCenter|Qt.AlignBottom)

        self.botFrame = QFrame(self.origFrame)
        self.botFrame.setObjectName(u"botFrame")
        self.botFrame.setStyleSheet(u"QLabel {\n"
"    font-family: \"Times New Roman\";\n"
"    font-size: 9pt;\n"
"    color: #54493E;\n"
"    text-decoration: underline;\n"
"}\n"
"QLabel:hover {\n"
"    color: #7A6C5B;  /* example hover color: lighter shade */\n"
"}\n"
"")
        self.botFrame.setFrameShape(QFrame.StyledPanel)
        self.botFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_18 = QVBoxLayout(self.botFrame)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 25, 35)
        self.aboutBtn = QLabel(self.botFrame)
        self.aboutBtn.setObjectName(u"aboutBtn")

        self.verticalLayout_18.addWidget(self.aboutBtn)


        self.verticalLayout_16.addWidget(self.botFrame, 0, Qt.AlignRight|Qt.AlignBottom)


        self.verticalLayout_11.addWidget(self.origFrame)


        self.verticalLayout_10.addWidget(self.backgroundFrame)

        self.stackedWidget.addWidget(self.HomePage)
        self.SignatoriesPage = QWidget()
        self.SignatoriesPage.setObjectName(u"SignatoriesPage")
        self.horizontalLayout_23 = QHBoxLayout(self.SignatoriesPage)
        self.horizontalLayout_23.setSpacing(0)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.frame_11 = QFrame(self.SignatoriesPage)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.NoFrame)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.verticalLayout_23 = QVBoxLayout(self.frame_11)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.frame_18 = QFrame(self.frame_11)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setFrameShape(QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Raised)

        self.verticalLayout_23.addWidget(self.frame_18)

        self.frame_19 = QFrame(self.frame_11)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setFrameShape(QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QFrame.Raised)

        self.verticalLayout_23.addWidget(self.frame_19)


        self.horizontalLayout_23.addWidget(self.frame_11)

        self.stackedWidget.addWidget(self.SignatoriesPage)
        self.activityListPage = QWidget()
        self.activityListPage.setObjectName(u"activityListPage")
        self.activityListPage.setStyleSheet(u"QFrame#activityListPage {\n"
"    border-image: url(:/bgs/images/ht3.png) 50 25 50 25 stretch stretch;\n"
"}\n"
"")
        self.horizontalLayout_9 = QHBoxLayout(self.activityListPage)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.listFrame = QFrame(self.activityListPage)
        self.listFrame.setObjectName(u"listFrame")
        self.listFrame.setStyleSheet(u"QFrame#listFrame {\n"
"    border-image: url(:/bgs/images/ht3.png) 50 25 50 25 stretch stretch;\n"
"}\n"
"")
        self.listFrame.setFrameShape(QFrame.NoFrame)
        self.listFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_20 = QVBoxLayout(self.listFrame)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.frame_26 = QFrame(self.listFrame)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setStyleSheet(u"QFrame {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}\n"
"")
        self.frame_26.setFrameShape(QFrame.NoFrame)
        self.frame_26.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_26)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(10, 0, 0, 0)
        self.recentDocuments = QLabel(self.frame_26)
        self.recentDocuments.setObjectName(u"recentDocuments")
        self.recentDocuments.setStyleSheet(u"QLabel{\n"
"    font-family: \"Times New Roman\";\n"
"    font-size: 17pt;\n"
"    color:rgb(41, 28, 14);\n"
"}\n"
"")

        self.horizontalLayout_12.addWidget(self.recentDocuments, 0, Qt.AlignTop)


        self.verticalLayout_20.addWidget(self.frame_26)

        self.frame_27 = QFrame(self.listFrame)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setStyleSheet(u"QFrame#frame_27 {\n"
"    border-image: url(:/bgs/images/ht3.png) 50 25 50 25 stretch stretch;\n"
"}\n"
"")
        self.frame_27.setFrameShape(QFrame.NoFrame)
        self.frame_27.setFrameShadow(QFrame.Raised)
        self.verticalLayout_21 = QVBoxLayout(self.frame_27)
        self.verticalLayout_21.setSpacing(0)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(15, 0, 15, 30)
        self.savedListWidget = QListWidget(self.frame_27)
        self.savedListWidget.setObjectName(u"savedListWidget")
        self.savedListWidget.setStyleSheet(u"/* Modify your QListWidget stylesheet to this */\n"
"QListWidget {\n"
"    color: #E1D4C2;\n"
"    font-family: \"Courier New\";\n"
"    font-size: 16px;\n"
"	background-image:url(:/bgs/images/ht3.png);\n"
"	background-position: center;\n"
"background-origin: content;\n"
"background-attachment: fixed;\n"
"\n"
"}\n"
"\n"
"QListWidget::item {\n"
"    padding: 6px;\n"
"\n"
"}\n"
"\n"
"QListWidget::item:hover {\n"
"        border: 1px solid rgb(41, 28, 14);\n"
"}\n"
"\n"
"")
        self.savedListWidget.setFrameShape(QFrame.Box)
        self.savedListWidget.setFrameShadow(QFrame.Sunken)
        self.savedListWidget.setLineWidth(3)
        self.savedListWidget.setModelColumn(0)
        self.savedListWidget.setWordWrap(True)

        self.verticalLayout_21.addWidget(self.savedListWidget)


        self.verticalLayout_20.addWidget(self.frame_27)


        self.horizontalLayout_9.addWidget(self.listFrame)

        self.stackedWidget.addWidget(self.activityListPage)
        self.activityLogPage = QWidget()
        self.activityLogPage.setObjectName(u"activityLogPage")
        self.horizontalLayout_10 = QHBoxLayout(self.activityLogPage)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.frame_24 = QFrame(self.activityLogPage)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setFrameShape(QFrame.StyledPanel)
        self.frame_24.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_22 = QHBoxLayout(self.frame_24)
        self.horizontalLayout_22.setSpacing(0)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.frame_25 = QFrame(self.frame_24)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setStyleSheet(u"background-color:rgb(255, 255, 255)")
        self.frame_25.setFrameShape(QFrame.NoFrame)
        self.frame_25.setFrameShadow(QFrame.Raised)
        self.frame_25.setLineWidth(0)
        self.verticalLayout_22 = QVBoxLayout(self.frame_25)
        self.verticalLayout_22.setSpacing(0)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(20, 20, 20, 5)
        self.frame_30 = QFrame(self.frame_25)
        self.frame_30.setObjectName(u"frame_30")
        self.frame_30.setFrameShape(QFrame.NoFrame)
        self.frame_30.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_21 = QHBoxLayout(self.frame_30)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.logTranscriptDisplay = QTextEdit(self.frame_30)
        self.logTranscriptDisplay.setObjectName(u"logTranscriptDisplay")
        self.logTranscriptDisplay.setStyleSheet(u"QTextEdit {\n"
"    font-family: \"Courier New\";\n"
"    font-size: 10pt;\n"
"    color: #54493E;\n"
"}\n"
"\n"
"")
        self.logTranscriptDisplay.setFrameShape(QFrame.Box)
        self.logTranscriptDisplay.setLineWidth(3)
        self.logTranscriptDisplay.setLineWrapColumnOrWidth(50)

        self.horizontalLayout_21.addWidget(self.logTranscriptDisplay)

        self.logMinutesDisplay = QTextEdit(self.frame_30)
        self.logMinutesDisplay.setObjectName(u"logMinutesDisplay")
        self.logMinutesDisplay.setStyleSheet(u"QTextEdit {\n"
"    font-family: \"Courier New\";\n"
"    font-size: 10pt;\n"
"    color: #54493E;\n"
"}\n"
"\n"
"")
        self.logMinutesDisplay.setFrameShape(QFrame.Box)
        self.logMinutesDisplay.setLineWidth(3)
        self.logMinutesDisplay.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.logMinutesDisplay.setLineWrapMode(QTextEdit.WidgetWidth)
        self.logMinutesDisplay.setLineWrapColumnOrWidth(50)

        self.horizontalLayout_21.addWidget(self.logMinutesDisplay)


        self.verticalLayout_22.addWidget(self.frame_30)

        self.frame_31 = QFrame(self.frame_25)
        self.frame_31.setObjectName(u"frame_31")
        self.frame_31.setFrameShape(QFrame.NoFrame)
        self.frame_31.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.frame_31)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 40)
        self.frame_32 = QFrame(self.frame_31)
        self.frame_32.setObjectName(u"frame_32")
        self.frame_32.setFrameShape(QFrame.NoFrame)
        self.frame_32.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.frame_32)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.returnLogBtn = QPushButton(self.frame_32)
        self.returnLogBtn.setObjectName(u"returnLogBtn")
        self.returnLogBtn.setMinimumSize(QSize(80, 30))
        self.returnLogBtn.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(78, 64, 50)\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:  rgb(185, 128, 118)\n"
"}\n"
"")
        self.returnLogBtn.setCursor(Qt.PointingHandCursor)
        self.returnLogBtn.setIcon(icon6)
        self.returnLogBtn.setIconSize(QSize(60, 16))
        self.returnLogBtn.setFlat(True)

        self.horizontalLayout_19.addWidget(self.returnLogBtn)


        self.horizontalLayout_18.addWidget(self.frame_32, 0, Qt.AlignLeft)

        self.frame_33 = QFrame(self.frame_31)
        self.frame_33.setObjectName(u"frame_33")
        self.frame_33.setFrameShape(QFrame.NoFrame)
        self.frame_33.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.frame_33)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.logGenerateBtn = QPushButton(self.frame_33)
        self.logGenerateBtn.setObjectName(u"logGenerateBtn")
        self.logGenerateBtn.setMinimumSize(QSize(100, 30))
        self.logGenerateBtn.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(78, 64, 50)\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:  rgb(167, 141, 120) \n"
"}\n"
"")
        self.logGenerateBtn.setCursor(Qt.PointingHandCursor)
        self.logGenerateBtn.setIcon(icon7)
        self.logGenerateBtn.setIconSize(QSize(70, 20))
        self.logGenerateBtn.setFlat(True)

        self.horizontalLayout_20.addWidget(self.logGenerateBtn)

        self.logSaveBtn = QPushButton(self.frame_33)
        self.logSaveBtn.setObjectName(u"logSaveBtn")
        self.logSaveBtn.setMinimumSize(QSize(60, 30))
        self.logSaveBtn.setStyleSheet(u"QPushButton {\n"
"    background-color:rgb(78, 64, 50)\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:rgb(185, 186, 143)\n"
"}")
        self.logSaveBtn.setCursor(Qt.PointingHandCursor)
        self.logSaveBtn.setIcon(icon8)
        self.logSaveBtn.setIconSize(QSize(36, 20))
        self.logSaveBtn.setFlat(True)

        self.horizontalLayout_20.addWidget(self.logSaveBtn)


        self.horizontalLayout_18.addWidget(self.frame_33, 0, Qt.AlignRight)


        self.verticalLayout_22.addWidget(self.frame_31)


        self.horizontalLayout_22.addWidget(self.frame_25)


        self.horizontalLayout_10.addWidget(self.frame_24)

        self.stackedWidget.addWidget(self.activityLogPage)

        self.verticalLayout_7.addWidget(self.stackedWidget)


        self.verticalLayout.addWidget(self.mainBodyContent)


        self.horizontalLayout.addWidget(self.mainBody)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.LogButton.setDefault(False)
        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText("")
        self.homeButton.setText("")
        self.LogButton.setText("")
        self.sideDrawerButton.setText("")
        self.minimizeWindow.setText("")
        self.maximizeWindow.setText("")
        self.close.setText("")
        self.minutesDisplay.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Generate Minutes of the Meeting...", None))
        self.replaceTextBtn.setText(QCoreApplication.translate("MainWindow", u"Find and Replace?", None))
        self.returnBtn.setText("")
        self.generateBtn.setText("")
        self.saveBtn.setText("")
        self.clearBtn.setText("")
        self.agendaInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Input Agenda (Optional):", None))
        self.attendeesInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Input Attendees (Optional):", None))
        self.transcriptDisplay.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Meeting Transcription...", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Assign Speaker", None))
        self.speakerNumber.setPlaceholderText(QCoreApplication.translate("MainWindow", u"eg. 01", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"to", None))
        self.speakerName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"eg. Elizabeth Guevarra", None))
        self.assignSpeakerBtn.setText(QCoreApplication.translate("MainWindow", u"Assign", None))
        self.uploadedFileLabel.setText("")
        self.uploadBtn.setText("")
        self.transcribeBtn.setText("")
        self.proceedBtn.setText("")
        self.getStartedBtn.setText("")
        self.aboutBtn.setText(QCoreApplication.translate("MainWindow", u"Need Tutorial? Click here.", None))
        self.recentDocuments.setText(QCoreApplication.translate("MainWindow", u"Recent Documents", None))
        self.logTranscriptDisplay.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Meeting Transcript...", None))
        self.logMinutesDisplay.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Minutes of the Meeting...", None))
        self.returnLogBtn.setText("")
        self.logGenerateBtn.setText("")
        self.logSaveBtn.setText("")
    # retranslateUi

