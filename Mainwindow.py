# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainwindowhhnHmZ.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1306, 776)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 1301, 731))
        font = QFont()
        font.setStyleStrategy(QFont.PreferAntialias)
        self.tabWidget.setFont(font)
        self.tab_0 = QWidget()
        self.tab_0.setObjectName(u"tab_0")
        self.line_4 = QFrame(self.tab_0)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setGeometry(QRect(10, 360, 571, 20))
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)
        self.pushButton_LoadFile = QPushButton(self.tab_0)
        self.pushButton_LoadFile.setObjectName(u"pushButton_LoadFile")
        self.pushButton_LoadFile.setGeometry(QRect(20, 20, 121, 41))
        font1 = QFont()
        font1.setPointSize(9)
        font1.setStyleStrategy(QFont.PreferAntialias)
        self.pushButton_LoadFile.setFont(font1)
        self.line_2 = QFrame(self.tab_0)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(10, 100, 571, 20))
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.formLayoutWidget = QWidget(self.tab_0)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(20, 160, 221, 61))
        self.FLayout_pagesInfo = QFormLayout(self.formLayoutWidget)
        self.FLayout_pagesInfo.setObjectName(u"FLayout_pagesInfo")
        self.FLayout_pagesInfo.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.FLayout_pagesInfo.setContentsMargins(0, 0, 0, 0)
        self.label_DetThresholdText = QLabel(self.formLayoutWidget)
        self.label_DetThresholdText.setObjectName(u"label_DetThresholdText")
        self.label_DetThresholdText.setFont(font1)
        self.label_DetThresholdText.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.FLayout_pagesInfo.setWidget(0, QFormLayout.LabelRole, self.label_DetThresholdText)

        self.doubleSpinBox_DetThreshold = QDoubleSpinBox(self.formLayoutWidget)
        self.doubleSpinBox_DetThreshold.setObjectName(u"doubleSpinBox_DetThreshold")
        self.doubleSpinBox_DetThreshold.setFont(font1)
        self.doubleSpinBox_DetThreshold.setDecimals(2)
        self.doubleSpinBox_DetThreshold.setMaximum(1.000000000000000)
        self.doubleSpinBox_DetThreshold.setSingleStep(0.010000000000000)
        self.doubleSpinBox_DetThreshold.setValue(0.200000000000000)

        self.FLayout_pagesInfo.setWidget(0, QFormLayout.FieldRole, self.doubleSpinBox_DetThreshold)

        self.label_BlurrSizeText = QLabel(self.formLayoutWidget)
        self.label_BlurrSizeText.setObjectName(u"label_BlurrSizeText")
        self.label_BlurrSizeText.setFont(font1)
        self.label_BlurrSizeText.setScaledContents(False)
        self.label_BlurrSizeText.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.FLayout_pagesInfo.setWidget(1, QFormLayout.LabelRole, self.label_BlurrSizeText)

        self.doubleSpinBox_BlurrSize = QDoubleSpinBox(self.formLayoutWidget)
        self.doubleSpinBox_BlurrSize.setObjectName(u"doubleSpinBox_BlurrSize")
        self.doubleSpinBox_BlurrSize.setFont(font1)
        self.doubleSpinBox_BlurrSize.setSingleStep(0.200000000000000)
        self.doubleSpinBox_BlurrSize.setValue(1.200000000000000)

        self.FLayout_pagesInfo.setWidget(1, QFormLayout.FieldRole, self.doubleSpinBox_BlurrSize)

        self.pushButton_Export = QPushButton(self.tab_0)
        self.pushButton_Export.setObjectName(u"pushButton_Export")
        self.pushButton_Export.setGeometry(QRect(440, 20, 121, 41))
        self.pushButton_Export.setFont(font1)
        self.lineEdit_OpenFile = QLineEdit(self.tab_0)
        self.lineEdit_OpenFile.setObjectName(u"lineEdit_OpenFile")
        self.lineEdit_OpenFile.setGeometry(QRect(20, 70, 541, 20))
        self.lineEdit_OpenFile.setReadOnly(True)
        self.line = QFrame(self.tab_0)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(570, 10, 20, 571))
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.horizontalLayoutWidget = QWidget(self.tab_0)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(20, 380, 321, 61))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_BlurrShapeText = QLabel(self.horizontalLayoutWidget)
        self.label_BlurrShapeText.setObjectName(u"label_BlurrShapeText")
        self.label_BlurrShapeText.setFont(font1)
        self.label_BlurrShapeText.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_BlurrShapeText)

        self.radioButton_BlurrShape_Ellipse = QRadioButton(self.horizontalLayoutWidget)
        self.radioButton_BlurrShape_Ellipse.setObjectName(u"radioButton_BlurrShape_Ellipse")
        self.radioButton_BlurrShape_Ellipse.setFont(font1)
        self.radioButton_BlurrShape_Ellipse.setChecked(True)

        self.horizontalLayout.addWidget(self.radioButton_BlurrShape_Ellipse)

        self.radioButton_BlurrShape_Rectangle = QRadioButton(self.horizontalLayoutWidget)
        self.radioButton_BlurrShape_Rectangle.setObjectName(u"radioButton_BlurrShape_Rectangle")
        self.radioButton_BlurrShape_Rectangle.setFont(font1)
        self.radioButton_BlurrShape_Rectangle.setChecked(False)

        self.horizontalLayout.addWidget(self.radioButton_BlurrShape_Rectangle)

        self.horizontalLayoutWidget_2 = QWidget(self.tab_0)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(20, 450, 541, 61))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_BlurrMethodText = QLabel(self.horizontalLayoutWidget_2)
        self.label_BlurrMethodText.setObjectName(u"label_BlurrMethodText")
        self.label_BlurrMethodText.setFont(font1)
        self.label_BlurrMethodText.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_BlurrMethodText)

        self.radioButton_BlurrMethod_Blurr = QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_BlurrMethod_Blurr.setObjectName(u"radioButton_BlurrMethod_Blurr")
        self.radioButton_BlurrMethod_Blurr.setFont(font1)
        self.radioButton_BlurrMethod_Blurr.setChecked(True)

        self.horizontalLayout_2.addWidget(self.radioButton_BlurrMethod_Blurr)

        self.radioButton_BlurrMethod_Mosaic = QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_BlurrMethod_Mosaic.setObjectName(u"radioButton_BlurrMethod_Mosaic")
        self.radioButton_BlurrMethod_Mosaic.setFont(font1)

        self.horizontalLayout_2.addWidget(self.radioButton_BlurrMethod_Mosaic)

        self.radioButton_BlurrMethod_Solid = QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_BlurrMethod_Solid.setObjectName(u"radioButton_BlurrMethod_Solid")
        self.radioButton_BlurrMethod_Solid.setFont(font1)

        self.horizontalLayout_2.addWidget(self.radioButton_BlurrMethod_Solid)

        self.radioButton_BlurrMethod_None = QRadioButton(self.horizontalLayoutWidget_2)
        self.radioButton_BlurrMethod_None.setObjectName(u"radioButton_BlurrMethod_None")
        self.radioButton_BlurrMethod_None.setFont(font1)

        self.horizontalLayout_2.addWidget(self.radioButton_BlurrMethod_None)

        self.formLayoutWidget_2 = QWidget(self.tab_0)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(40, 530, 175, 31))
        self.FLayout_pagesInfo_2 = QFormLayout(self.formLayoutWidget_2)
        self.FLayout_pagesInfo_2.setObjectName(u"FLayout_pagesInfo_2")
        self.FLayout_pagesInfo_2.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.FLayout_pagesInfo_2.setContentsMargins(0, 0, 0, 0)
        self.label_MosaicSizeText = QLabel(self.formLayoutWidget_2)
        self.label_MosaicSizeText.setObjectName(u"label_MosaicSizeText")
        self.label_MosaicSizeText.setFont(font1)
        self.label_MosaicSizeText.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.FLayout_pagesInfo_2.setWidget(0, QFormLayout.LabelRole, self.label_MosaicSizeText)

        self.spinBox_MosaicSize = QSpinBox(self.formLayoutWidget_2)
        self.spinBox_MosaicSize.setObjectName(u"spinBox_MosaicSize")
        self.spinBox_MosaicSize.setFont(font1)
        self.spinBox_MosaicSize.setMinimum(1)
        self.spinBox_MosaicSize.setMaximum(9999999)
        self.spinBox_MosaicSize.setValue(20)

        self.FLayout_pagesInfo_2.setWidget(0, QFormLayout.FieldRole, self.spinBox_MosaicSize)

        self.line_3 = QFrame(self.tab_0)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setGeometry(QRect(10, 230, 571, 20))
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.checkBox_RemoveAudioTracks = QCheckBox(self.tab_0)
        self.checkBox_RemoveAudioTracks.setObjectName(u"checkBox_RemoveAudioTracks")
        self.checkBox_RemoveAudioTracks.setGeometry(QRect(20, 130, 211, 20))
        self.checkBox_RemoveAudioTracks.setFont(font1)
        self.verticalLayoutWidget = QWidget(self.tab_0)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(599, 10, 691, 571))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.graphicsView_Preview = QGraphicsView(self.verticalLayoutWidget)
        self.graphicsView_Preview.setObjectName(u"graphicsView_Preview")
        self.graphicsView_Preview.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.graphicsView_Preview.setSceneRect(QRectF(0, 0, 559, 480))

        self.verticalLayout.addWidget(self.graphicsView_Preview)

        self.horizontalSlider_Preview = QSlider(self.verticalLayoutWidget)
        self.horizontalSlider_Preview.setObjectName(u"horizontalSlider_Preview")
        self.horizontalSlider_Preview.setMaximum(1000)
        self.horizontalSlider_Preview.setSingleStep(1)
        self.horizontalSlider_Preview.setPageStep(1)
        self.horizontalSlider_Preview.setOrientation(Qt.Horizontal)

        self.verticalLayout.addWidget(self.horizontalSlider_Preview)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_Preview_Start = QLabel(self.verticalLayoutWidget)
        self.label_Preview_Start.setObjectName(u"label_Preview_Start")
        self.label_Preview_Start.setFont(font1)
        self.label_Preview_Start.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_Preview_Start)

        self.label_Preview_Current = QLabel(self.verticalLayoutWidget)
        self.label_Preview_Current.setObjectName(u"label_Preview_Current")
        self.label_Preview_Current.setFont(font1)
        self.label_Preview_Current.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_Preview_Current)

        self.label_Preview_End = QLabel(self.verticalLayoutWidget)
        self.label_Preview_End.setObjectName(u"label_Preview_End")
        self.label_Preview_End.setFont(font1)
        self.label_Preview_End.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_Preview_End)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_Preview_Start_Frame = QLabel(self.verticalLayoutWidget)
        self.label_Preview_Start_Frame.setObjectName(u"label_Preview_Start_Frame")
        self.label_Preview_Start_Frame.setFont(font1)
        self.label_Preview_Start_Frame.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.label_Preview_Start_Frame)

        self.spinBox_Preview_Current_Frame = QSpinBox(self.verticalLayoutWidget)
        self.spinBox_Preview_Current_Frame.setObjectName(u"spinBox_Preview_Current_Frame")
        self.spinBox_Preview_Current_Frame.setFont(font1)
        self.spinBox_Preview_Current_Frame.setAlignment(Qt.AlignCenter)
        self.spinBox_Preview_Current_Frame.setMaximum(999999999)

        self.horizontalLayout_9.addWidget(self.spinBox_Preview_Current_Frame)

        self.label_Preview_End_Frame = QLabel(self.verticalLayoutWidget)
        self.label_Preview_End_Frame.setObjectName(u"label_Preview_End_Frame")
        self.label_Preview_End_Frame.setFont(font1)
        self.label_Preview_End_Frame.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.label_Preview_End_Frame)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.pushButton_ResetValues = QPushButton(self.tab_0)
        self.pushButton_ResetValues.setObjectName(u"pushButton_ResetValues")
        self.pushButton_ResetValues.setGeometry(QRect(160, 20, 121, 41))
        self.pushButton_ResetValues.setFont(font1)
        self.line_5 = QFrame(self.tab_0)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setGeometry(QRect(10, 0, 571, 20))
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)
        self.line_11 = QFrame(self.tab_0)
        self.line_11.setObjectName(u"line_11")
        self.line_11.setGeometry(QRect(0, 10, 20, 571))
        self.line_11.setFrameShape(QFrame.VLine)
        self.line_11.setFrameShadow(QFrame.Sunken)
        self.formLayoutWidget_5 = QWidget(self.tab_0)
        self.formLayoutWidget_5.setObjectName(u"formLayoutWidget_5")
        self.formLayoutWidget_5.setGeometry(QRect(20, 250, 321, 101))
        self.FLayout_pagesInfo_5 = QFormLayout(self.formLayoutWidget_5)
        self.FLayout_pagesInfo_5.setObjectName(u"FLayout_pagesInfo_5")
        self.FLayout_pagesInfo_5.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.FLayout_pagesInfo_5.setContentsMargins(0, 0, 0, 0)
        self.checkBox_Downscale = QCheckBox(self.formLayoutWidget_5)
        self.checkBox_Downscale.setObjectName(u"checkBox_Downscale")
        self.checkBox_Downscale.setFont(font1)

        self.FLayout_pagesInfo_5.setWidget(0, QFormLayout.LabelRole, self.checkBox_Downscale)

        self.label_OriginalResText = QLabel(self.formLayoutWidget_5)
        self.label_OriginalResText.setObjectName(u"label_OriginalResText")
        self.label_OriginalResText.setFont(font1)
        self.label_OriginalResText.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.FLayout_pagesInfo_5.setWidget(2, QFormLayout.LabelRole, self.label_OriginalResText)

        self.lineEdit_OriginalRes = QLineEdit(self.formLayoutWidget_5)
        self.lineEdit_OriginalRes.setObjectName(u"lineEdit_OriginalRes")
        self.lineEdit_OriginalRes.setFont(font1)
        self.lineEdit_OriginalRes.setAlignment(Qt.AlignCenter)
        self.lineEdit_OriginalRes.setReadOnly(True)

        self.FLayout_pagesInfo_5.setWidget(2, QFormLayout.FieldRole, self.lineEdit_OriginalRes)

        self.label_NewResText = QLabel(self.formLayoutWidget_5)
        self.label_NewResText.setObjectName(u"label_NewResText")
        self.label_NewResText.setFont(font1)
        self.label_NewResText.setScaledContents(False)
        self.label_NewResText.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.FLayout_pagesInfo_5.setWidget(3, QFormLayout.LabelRole, self.label_NewResText)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.spinBox_NewResW = QSpinBox(self.formLayoutWidget_5)
        self.spinBox_NewResW.setObjectName(u"spinBox_NewResW")
        self.spinBox_NewResW.setFont(font1)
        self.spinBox_NewResW.setAlignment(Qt.AlignCenter)
        self.spinBox_NewResW.setMinimum(1)
        self.spinBox_NewResW.setMaximum(100000)

        self.horizontalLayout_8.addWidget(self.spinBox_NewResW)

        self.label_11 = QLabel(self.formLayoutWidget_5)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font1)
        self.label_11.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.label_11)

        self.spinBox_NewResH = QSpinBox(self.formLayoutWidget_5)
        self.spinBox_NewResH.setObjectName(u"spinBox_NewResH")
        self.spinBox_NewResH.setFont(font1)
        self.spinBox_NewResH.setAlignment(Qt.AlignCenter)
        self.spinBox_NewResH.setMinimum(1)
        self.spinBox_NewResH.setMaximum(100000)

        self.horizontalLayout_8.addWidget(self.spinBox_NewResH)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer)


        self.FLayout_pagesInfo_5.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_8)

        self.line_12 = QFrame(self.tab_0)
        self.line_12.setObjectName(u"line_12")
        self.line_12.setGeometry(QRect(10, 570, 571, 20))
        self.line_12.setFrameShape(QFrame.HLine)
        self.line_12.setFrameShadow(QFrame.Sunken)
        self.textBrowser = QTextBrowser(self.tab_0)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(350, 250, 221, 101))
        self.label_12 = QLabel(self.tab_0)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(260, 150, 311, 41))
        self.label_13 = QLabel(self.tab_0)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(260, 190, 311, 41))
        self.pushButton_Export_2 = QPushButton(self.tab_0)
        self.pushButton_Export_2.setObjectName(u"pushButton_Export_2")
        self.pushButton_Export_2.setGeometry(QRect(300, 20, 121, 41))
        self.pushButton_Export_2.setFont(font1)
        self.textEdit_ConsoleOutput = QTextEdit(self.tab_0)
        self.textEdit_ConsoleOutput.setObjectName(u"textEdit_ConsoleOutput")
        self.textEdit_ConsoleOutput.setGeometry(QRect(10, 590, 1281, 91))
        self.textEdit_ConsoleOutput.setAutoFillBackground(False)
        self.textEdit_ConsoleOutput.setReadOnly(True)
        self.tabWidget.addTab(self.tab_0, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_0), u";)")
        self.tab_1 = QWidget()
        self.tab_1.setObjectName(u"tab_1")
        self.textBrowser_4 = QTextBrowser(self.tab_1)
        self.textBrowser_4.setObjectName(u"textBrowser_4")
        self.textBrowser_4.setGeometry(QRect(20, 20, 1261, 671))
        self.textBrowser_4.setHtml(u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<h1 style=\" margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"deface-gui\"></a><span style=\" font-size:xx-large; font-weight:600;\">D</span><span style=\" font-size:xx-large; font-weight:600;\">eface-GUI</span></h1>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">This projet is a GUI for mdraw's &quot;deface&quot; command line tool with frame-per-frame tools, allowing for automatic and quick face censoring form videos. Frame censoring may be necessary for activities such as transparently shari"
                        "ng video training data for Neural Nets or reporter activity without compromising passerby's privacy</span></p>\n"
"<h1 style=\" margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"attributions-\"></a><span style=\" font-size:xx-large; font-weight:600;\">A</span><span style=\" font-size:xx-large; font-weight:600;\">ttributions:</span></h1>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">This program is just a GUI for the command tool deface by mdraw. You may find more projects on [</span><a href=\"https://github.com/vicent-b\"><span style=\" font-size:9pt; text-decoration: underline; color:#0000ff;\">https://github.com/vicent-b</span></a><span style=\" font-size:9pt;\">]</span></p>\n"
"<h1 style=\" margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"information-\"></"
                        "a><span style=\" font-size:xx-large; font-weight:600;\">I</span><span style=\" font-size:xx-large; font-weight:600;\">nformation:</span></h1>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">You may upload a single video or an image. The image on the right shows the conversion of a given image or video frame (that may be changed using the slider), while also showing the face detection confidence. The autoconvert button (soon to come) allows to select a bunch of files and convert them quickly with the default settings. The algorithm looks for faces within each image/frame and dettects them with a given confidence (0-&gt;1). They are blurred only if the confidence is above the chosen threshold. By changing the threshold you may elliminate false negatives (faces not detected as such) while minimising false positives (non-faces dettected as faces). You may donwscale the video before processing to make it f"
                        "aster or correct tome errors. You have the explanation in the textbox next to the option. Blurr method and size may also be chosen. Click export to export the video or images. Video defacing takes a while, so you may see the progress bar on the console window. </span></p>\n"
"<h1 style=\" margin-top:18px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"installation-and-gpu-acceleration-guide\"></a><span style=\" font-size:xx-large; font-weight:600;\">I</span><span style=\" font-size:xx-large; font-weight:600;\">nstallation and GPU acceleration guide</span></h1>\n"
"<h2 style=\" margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"windows\"></a><span style=\" font-size:x-large; font-weight:600;\">W</span><span style=\" font-size:x-large; font-weight:600;\">indows</span></h2>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-ind"
                        "ent:0px;\"><span style=\" font-size:9pt;\">In order to use the program, you need to install the Python programming language interpreter from its </span><a href=\"www.python.org\"><span style=\" font-size:9pt; text-decoration: underline; color:#0000ff;\">webpage</span></a><span style=\" font-size:9pt;\">. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">It is important to select the option &quot;Add python.exe to PATH&quot;. This adds the program location to the PATH variable, which windows uses to search for important files or programs</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Then, you must open the command line (write &quot;cmd&quot; in the windows menu search bar) to install the rewuiered packages usong &quot;pip&quot;. Pip is a program that comes with python th"
                        "at allows to download and install complemenrs if they are not already installed. Write the following commands:</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:9pt;\">pip install deface   #original cmd-based deface program</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:9pt;\">pip install PySide6  #Graphic User Interface tools</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Courier New'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Moreover, video prpcessing is too slow if "
                        "done on the CPU, so it is better to use the graphics card. In windows you may use direct-ml:</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:9pt;\">pip install onnx onnxruntime-directml</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Courier New'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Finally, if you have an NVIDIA graphics card and CUDA installed, you may instead use:</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:9pt;\">pip install onnx onnxruntime-gpu</span></p"
                        ">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Courier New'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">To ensure the graphics card is being used instead of the CPU, use the Task Manager when processing a file</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Finally, download the whole folder and open (run) &quot;deface_GUI.py&quot; with Python</span></p>\n"
"<h2 style=\" margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a name=\"linux\"></a><span style=\" font-size:x-large; font-weight:600;\">L</span><span style=\" font-size:x-large; font-weight:600;\">inux</span></h2>\n"
""
                        "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Let's be frank: I trust you are tech savvy enough to install Python and the listed dependencies for Windows users</span></p></body></html>")
        self.tabWidget.addTab(self.tab_1, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1306, 26))
        self.menubar.setDefaultUp(False)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Deface GUI", None))
        self.pushButton_LoadFile.setText(QCoreApplication.translate("MainWindow", u"LOAD VIDEO", None))
        self.label_DetThresholdText.setText(QCoreApplication.translate("MainWindow", u"Detection threshold:", None))
        self.label_BlurrSizeText.setText(QCoreApplication.translate("MainWindow", u"Blurr size (relative):", None))
        self.pushButton_Export.setText(QCoreApplication.translate("MainWindow", u"EXPORT", None))
        self.label_BlurrShapeText.setText(QCoreApplication.translate("MainWindow", u"Blurr shape:", None))
        self.radioButton_BlurrShape_Ellipse.setText(QCoreApplication.translate("MainWindow", u"Ellipse", None))
        self.radioButton_BlurrShape_Rectangle.setText(QCoreApplication.translate("MainWindow", u"Rectangle", None))
        self.label_BlurrMethodText.setText(QCoreApplication.translate("MainWindow", u"Blurr method:", None))
        self.radioButton_BlurrMethod_Blurr.setText(QCoreApplication.translate("MainWindow", u"Blurr", None))
        self.radioButton_BlurrMethod_Mosaic.setText(QCoreApplication.translate("MainWindow", u"Mosaic", None))
        self.radioButton_BlurrMethod_Solid.setText(QCoreApplication.translate("MainWindow", u"Solid black", None))
        self.radioButton_BlurrMethod_None.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.label_MosaicSizeText.setText(QCoreApplication.translate("MainWindow", u"Mosaic size:", None))
        self.checkBox_RemoveAudioTracks.setText(QCoreApplication.translate("MainWindow", u"Remove audio tracks too", None))
        self.label_Preview_Start.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.label_Preview_Current.setText(QCoreApplication.translate("MainWindow", u"xx:xx:xx", None))
        self.label_Preview_End.setText(QCoreApplication.translate("MainWindow", u"ff:ff:ff", None))
        self.label_Preview_Start_Frame.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_Preview_End_Frame.setText(QCoreApplication.translate("MainWindow", u"FFFFFF", None))
        self.pushButton_ResetValues.setText(QCoreApplication.translate("MainWindow", u"Reset values\n"
"to default", None))
        self.checkBox_Downscale.setText(QCoreApplication.translate("MainWindow", u"Downscale?", None))
        self.label_OriginalResText.setText(QCoreApplication.translate("MainWindow", u"Resolution:", None))
        self.label_NewResText.setText(QCoreApplication.translate("MainWindow", u"Downscale to Res:", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"x", None))
        self.textBrowser.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">IMPORTANT: Downscaling before processing does not affect the exorting resolution, it only affects the face-finding process. Lower resolution implies faster processing, but too much downscaling may miss smaller faces. However, the face-finding model has not been trained with with large images and may also have probles processing resolutions bigger than 720p(1280x720). It is important to keep the original aspect ratio, otherwise faces will be distorted and may be missed</p></body></html>", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Lower threshold means more false positives, while a \n"
"higher threshold implies more false negatives.", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Relative blurring size, proportional to face size.", None))
        self.pushButton_Export_2.setText(QCoreApplication.translate("MainWindow", u"Autoconvert\n"
"multiple files", None))
        self.textEdit_ConsoleOutput.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&gt;&gt;</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), QCoreApplication.translate("MainWindow", u"Info", None))
    # retranslateUi

