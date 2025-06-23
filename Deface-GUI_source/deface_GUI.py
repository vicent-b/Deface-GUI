import os
import sys
from enum import Enum
import math
import datetime
import numpy as np
import av
import imageio.v2 as iio
#import Lib.deface as deface #important to import as just deface, otherwise recursive calls within the package fail
#import deface.deface as deface
from deface import deface as deface
import QueueStreams as QS
import threading
import mimetypes

from Mainwindow import *




DebugMode:bool = False
def DEBUG(content):
    if(not DebugMode):
        return
    print("DEBUG: ", end="")
    print(content  , end="")
    print("\n"     , end="")



# INDEX
# -Window class and init
# -GLOBAL VARS
# -BASIC UTIL FUNCTIONS
# -BASIC GUI FUNCTIONS
# -COMPLEX FUNCTIONS
# -GUI EVENTS (Common code)
# -GUI EVENTS
# -MAIN PROGRAM AND AUTOTEST
#

#--------------------------------------------------------------------------------------------
##Window class and init

class myQtApp_MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

#--------------------------------------------------------------------------------------------
class BlurrShape_t(Enum):
    ELLIPSE = 0
    RECTANGLE = 1

class BlurrMethod_t(Enum):
    NONE = 0
    BLURR = 1
    MOSAIC = 2
    SOLID_BLACK = 3


class DefaceOptions_t:
    def __init__(self, DetectionThreshold:float = 0.2, BlurrSize:float = 1.3, RemoveAudioTracks:bool = False, Downscale:bool = False, DownscaleW:int = 1, DownscaleH:int = 1, BlurrShapeID:int = BlurrShape_t.ELLIPSE.value, BlurrMethodID:int = BlurrMethod_t.BLURR.value, MosaicSize:int=20):
        self.DetectionThreshold:float = DetectionThreshold
        self.BlurrSize:float = BlurrSize
        self.RemoveAudioTracks:bool = RemoveAudioTracks
        self.Downscale:bool = Downscale
        self.DownscaleW:int = DownscaleW
        self.DownscaleH:int = DownscaleH
        self.BlurrShapeID:int = BlurrShapeID
        self.BlurrMethodID:int = BlurrMethodID
        self.MosaicSize:int = MosaicSize
        self.dets_cache = None
    
    def set(self, DetectionThreshold:float = 0.2, BlurrSize:float = 1.3, RemoveAudioTracks:bool = False, Downscale:bool = False, DownscaleW:int = 1, DownscaleH:int = 1, BlurrShapeID:int = BlurrShape_t.ELLIPSE.value, BlurrMethodID:int = BlurrMethod_t.BLURR.value, MosaicSize:int=20):
        self.DetectionThreshold = DetectionThreshold
        self.BlurrSize = BlurrSize
        self.RemoveAudioTracks = RemoveAudioTracks
        self.Downscale = self.Downscale
        self.DownscaleW = DownscaleW
        self.DownscaleH = DownscaleH
        self.BlurrShapeID = BlurrShapeID
        self.BlurrMethodID = BlurrMethodID
        self.MosaicSize = MosaicSize
        self.dets_cache = None
    
    def setDO(self, DO):
        self.set(DO.DetectionThreshold, DO.BlurrSize, DO.RemoveAudioTracks, DO.Downscale, DO.DownscaleW, DO.DownscaleH, DO.BlurrShapeID, DO.BlurrMethodID, DO.MosaicSize)

        DEBUG("DO_SET")

    def generateOptionsStringArray(self):
        varArray=[]

        varArray.append("--thresh")
        varArray.append(str(self.DetectionThreshold))

        varArray.append("--mask-scale")
        varArray.append(str(self.BlurrSize))

        if(not self.RemoveAudioTracks):
            varArray.append("--keep-audio")
        
        if(self.Downscale):
            varArray.append("--scale")
            varArray.append(str(self.DownscaleW)+"x"+str(self.DownscaleH))



        if(self.BlurrShapeID == BlurrShape_t.RECTANGLE.value):
            varArray.append("--boxes")
        
        varArray.append("--replacewith")
        varArray.append(["none", "blur", "mosaic", "solid"][self.BlurrMethodID])

        if(self.BlurrMethodID == BlurrMethod_t.MOSAIC.value):
            varArray.append("--mosaicsize")
            varArray.append(str(self.MosaicSize))
        
        return varArray



class MediaFile_t:
    def __init__(self, FullPath:str):
        self.FullPath:str = FullPath
        self.FileName:str = os.path.basename(FullPath)
        self.Folder:str = os.path.dirname(FullPath)
        self.FileNameNoExt:str=""
        self.Extension:str =""
        self.FileNameNoExt, self.Extension = os.path.splitext(self.FileName)

        video_container = av.open(FullPath)
        video_stream=next(s for s in video_container.streams if s.type == 'video')
        self.durationSeconds:float = float(video_stream.duration * video_stream.time_base) if video_stream is not None and video_stream.duration is not None else None
        aproxNFrames:int = video_stream.frames
        video_container.close()

        filetype = mimetypes.guess_type(FullPath)[0]
        self.IsImage:bool = (filetype.startswith("image"))
        
        if not self.IsImage:
            self.iioHandler = iio.imopen(FullPath, "r", plugin="pyav")
        else:
            self.iioHandler = iio.imopen(FullPath, "r")

        if(aproxNFrames is None or aproxNFrames == 0):
            self.NFrames:int = self.CountExactFrames(6)
        else:
            self.NFrames:int = self.CountExactFrames(math.floor(math.log(aproxNFrames, 5)))

        DEBUG(self.NFrames)

        self.framerate:float = self.NFrames/self.durationSeconds if self.durationSeconds is not None else None
        self.CurrentFrameIndex:int = 0 
        self.CurrentFrameCache = self.iioHandler.read(index=0)
        DEBUG(self.CurrentFrameIndex)
        self.CurrentFrameCache = self.iioHandler.read(index=self.CurrentFrameIndex)

        self.width:int  = 0
        self.height:int = 0

        probeimage=self.CurrentFrameCache
        if(probeimage.ndim == 2):
            self.height, self.width = probeimage.shape
        elif (probeimage.ndim == 3):
            self.height, self.width,_ = probeimage.shape


    def UpdateCurrentFrame(self, frameNum:int):
        frameNum = frameNum if (frameNum < self.NFrames) else self.NFrames
        if(frameNum == self.CurrentFrameIndex):
            return
        self.CurrentFrameIndex = frameNum
        self.CurrentFrameCache = self.iioHandler.read(index=self.CurrentFrameIndex)

        
    def currentTimeSeconds(self):
        return float(self.CurrentFrameIndex*self.durationSeconds/self.NFrames) if self.durationSeconds is not None else None
    
    def CountExactFrames(self, digitPower=0, base=0):
        idx:int=base
        increment=5**digitPower #If done in powers of 10, it takes many cycles for a single digit, if done for powers of 2, it takes many digits (digits are fixed in the code, so it will take longer for shorter videos)

        while(True):
            idx_old:int=idx
            idx += increment
            DEBUG("idx: "+str(idx)+" base: "+str(base)+" dP: "+str(digitPower))
            try:
                self.iioHandler.read(index=idx)
            except:
                if(digitPower==0):
                    return idx
                else:
                    return self.CountExactFrames(digitPower-1,idx_old)
            



##GLOBAL VARS

DefaceOptions:DefaceOptions_t = DefaceOptions_t()
MediaFile:MediaFile_t = None

File_LastSelectedFolder_Load:str = ""
File_LastSelectedFolder_Save:str = ""

centerface = deface.CenterFace(in_shape=None, backend='auto') #cached

#window
app=QApplication()
MainWindow=myQtApp_MainWindow()
try: MainWindow.setWindowIcon(QIcon("./Icon/Icon1-16x16-24x24-32x32-48x48-256x256.ico"))
except: None


RadioButtonCollection_BlurrShape=[
    MainWindow.radioButton_BlurrShape_Ellipse,
    MainWindow.radioButton_BlurrShape_Rectangle
    ]

RadioButtonCollection_BlurrMethod=[
    MainWindow.radioButton_BlurrMethod_None,
    MainWindow.radioButton_BlurrMethod_Blurr,
    MainWindow.radioButton_BlurrMethod_Mosaic,
    MainWindow.radioButton_BlurrMethod_Solid
    ]

#thread coordination
SEMAPHORE_spinBox_ScrollBar_Preview:bool = False #When frame number is edited, slider value is changed. When slider moves, new frame number is displayed. This semaphore ensures framenumber is not edited again when slider is changed is

stdout_emitter:QS.streamEmitter = None
stdout_receiver:QS.streamReceiver = None
stdout_thread = None

deface_thread = None

#Consts
ADMITTED_FILE_EXTENSIONS_PATTERN="Video (*.mov *.avo *.mpg *.mp4 *.mkv *.wmv);;Common images (*.jpg *.jpeg *.png *.tiff *.bmp);;Any files (*)"

#--------------------------------------------------------------------------------------------
##BASIC UTIL FUNCTIONS

def framenum2Seconds(NFrame, MF:MediaFile_t):
    return float(NFrame)/float(MF.NFrames-1)*MF.durationSeconds

def seconds_to_hhmmssmm(sec):
    return str(datetime.timedelta(seconds=sec))


def ImageIO_to_QImage(image):
    #Convert imageio (NumPy) image to QImage, supporting grayscale, RGB, RGBA.

    if image.ndim == 2: #GRAYSCALE
        # Grayscale
        height, width = image.shape
        image = np.require(image, np.uint8, 'C')
        return QImage(image.data, width, height, width, QImage.Format_Grayscale8)

    elif image.ndim == 3: #RGB/RGBA
        height, width, channels = image.shape
        image = np.require(image, np.uint8, 'C')

        if channels == 3:
            # RGB
            bytes_per_line = 3 * width
            return QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        elif channels == 4:
            # RGBA
            bytes_per_line = 4 * width
            return QImage(image.data, width, height, bytes_per_line, QImage.Format_RGBA8888)

    raise ValueError(f"Unsupported image format with shape: {image.shape}")

def VideoGetFrame(video, N:int):
    frame = None
    return frame


def VideoGetRes(video):
    return 0

#--------------------------------------------------------------------------------------------
##BASIC GUI FUNCTIONS

def ManipulateStdoutQueue(queueElement):
    global MainWindow
    s=queueElement[0]
    #MainWindow.textEdit_ConsoleOutput.append(s)
    MainWindow.textEdit_ConsoleOutput.moveCursor (QTextCursor.End)
    MainWindow.textEdit_ConsoleOutput.insertPlainText (s)
    MainWindow.textEdit_ConsoleOutput.moveCursor (QTextCursor.End)


def OverloadStdout():
    global stdout_emitter
    global stdout_receiver
    global stdout_thread

    sharedQueue = QS.Queue()
    ##sys.stdout = QS.streamEmitter(sharedQueue)
    ##sys.stderr = sys.stdout
    sys.stderr = QS.streamEmitter(sharedQueue)
    stdout_receiver = QS.streamReceiver(sharedQueue, ManipulateStdoutQueue)

    stdout_thread = threading.Thread(target = lambda:stdout_receiver.run(), daemon=True)
    stdout_thread.start()


def ReadDefaceOptions(DO: DefaceOptions_t):
    
    BlurrShapeID:int = 0
    BlurrMethodID:int = 0
    
    for i in range(len(RadioButtonCollection_BlurrShape)):
        if(RadioButtonCollection_BlurrShape[i].isChecked()):
            BlurrShapeID = i
            break

    for i in range(len(RadioButtonCollection_BlurrMethod)):
        if(RadioButtonCollection_BlurrMethod[i].isChecked()):
            BlurrMethodID = i
            break

    DO.set(
        MainWindow.doubleSpinBox_DetThreshold.value(),
        MainWindow.doubleSpinBox_BlurrSize.value(),
        MainWindow.checkBox_RemoveAudioTracks.isChecked(),
        MainWindow.checkBox_Downscale.isChecked(),
        MainWindow.spinBox_NewResW.value(),
        MainWindow.spinBox_NewResH.value(),
        BlurrShapeID,
        BlurrMethodID,
        MainWindow.spinBox_MosaicSize.value()
    )

    
    
def SetDefaceOptions(DO: DefaceOptions_t):
    MainWindow.doubleSpinBox_DetThreshold.setValue(DO.DetectionThreshold)
    MainWindow.doubleSpinBox_BlurrSize.setValue(DO.BlurrSize)
    MainWindow.checkBox_RemoveAudioTracks.setChecked(DO.RemoveAudioTracks)
    MainWindow.checkBox_Downscale.setChecked(DO.Downscale)
    MainWindow.spinBox_NewResW.setValue(DO.DownscaleW)
    MainWindow.spinBox_NewResH.setValue(DO.DownscaleH)
    RadioButtonCollection_BlurrShape[DO.BlurrShapeID].setChecked(True)
    RadioButtonCollection_BlurrMethod[DO.BlurrMethodID].setChecked(True)
    MainWindow.spinBox_MosaicSize.setValue(DO.MosaicSize)
    

def SlideBar2FrameNum(MF:MediaFile_t, Slidebar=MainWindow.horizontalSlider_Preview):
    Pos=Slidebar.sliderPosition()
    value=float(Pos-Slidebar.minimum())/float(Slidebar.maximum()-Slidebar.minimum())
    return round(value*(MF.NFrames-1))

def FrameNum2SlideBar(FrameNum:int, MF:MediaFile_t, Slidebar=MainWindow.horizontalSlider_Preview):
    Pos=Slidebar.sliderPosition()
    value = float(FrameNum)/float(MF.NFrames-1)
    return round(value*(Slidebar.maximum()-Slidebar.minimum())+Slidebar.minimum())

def UpdateSlidebar(MF: MediaFile_t):
    global MainWindow
    if(MF.IsImage):
        return

    MainWindow.label_Preview_End.setText(seconds_to_hhmmssmm(MF.durationSeconds))
    MainWindow.label_Preview_End_Frame.setText(str(MF.NFrames-1))
    
    MainWindow.horizontalSlider_Preview.setValue(0)
    MainWindow.horizontalSlider_Preview.setMinimum(0)
    MainWindow.horizontalSlider_Preview.setMaximum(MF.durationSeconds*2)

    
    MainWindow.label_Preview_Current.setText(seconds_to_hhmmssmm(framenum2Seconds(MF.CurrentFrameIndex, MF)))
    MainWindow.spinBox_Preview_Current_Frame.setValue(MF.CurrentFrameIndex)
    MainWindow.spinBox_Preview_Current_Frame.setMaximum(MF.NFrames-1)

    DEBUG("SlidebarUpdated")   

def DisplayCurrentResolution(W:int,H:int):
    global MainWindow
    MainWindow.lineEdit_OriginalRes.setText(str(W)+" x "+str(H))

def DisplayQImage(qimage, scale=1):
    global MainWindow
    scale=1
    """
    GV = MainWindow.graphicsView_Preview
    GV.setSceneRect(0,0,GV.width()*scale,GV.height()*scale)


    pixmap = QPixmap.fromImage(qimage)
    scene = QGraphicsScene()
    scene.setSceneRect(GV.sceneRect())
    pixmap=pixmap.scaledToWidth(GV.width()*scale)
    pixmap_item = QGraphicsPixmapItem(pixmap)
    pixmap_item.setPos(0, 0)
    
    scene.addItem(pixmap_item)
    GV.setScene(scene)
    DEBUG(pixmap_item.pos())
    GV.fitInView(pixmap_item, Qt.KeepAspectRatio)
    """
    GV = MainWindow.graphicsView_Preview


    pixmap = QPixmap.fromImage(qimage)
    GV.setSceneRect(0,0,pixmap.width(), pixmap.height())
    scene = QGraphicsScene()
    scene.setSceneRect(GV.sceneRect())
    pixmap_item = QGraphicsPixmapItem(pixmap)
    pixmap_item.setPos(0, 0)
    
    scene.addItem(pixmap_item)
    GV.setScene(scene)
    DEBUG(pixmap_item.pos())
    GV.fitInView(pixmap_item, Qt.KeepAspectRatio)



def DisplayedImageScale(scale):
    global MainWindow
    GV = MainWindow.graphicsView_Preview
    #GV.setSceneRect(0,0,GV.width()*scale,GV.height()*scale)
    #GV.scene().scaledToWidth(GV.width()*scale)
    #GV.scene().setSceneRect(GV.sceneRect())
    GV.scale(scale,scale)


def DisplayIioImage(iioimage):
    qimage = ImageIO_to_QImage(iioimage)
    DisplayQImage(qimage)

#--------------------------------------------------------------------------------------------
##COMPLEX FUNCTIONS


def AnonimizeFrame(frame, DO:DefaceOptions_t, DrawScores:bool, dets=None):
    global centerface
    newframe=frame.copy()

    if(dets is None):
        if(centerface is None):
            centerface = deface.CenterFace(in_shape=None, backend='auto')
        dets, _ = centerface(newframe, threshold=DO.DetectionThreshold)
        DO.dets_cache = dets

    deface.anonymize_frame(
        dets = dets,
        frame = newframe,
        mask_scale = DO.BlurrSize,
        replacewith = ["none", "blur", "mosaic", "solid"][DO.BlurrMethodID],
        ellipse = (DO.BlurrShapeID==BlurrShape_t.ELLIPSE.value),
        draw_scores = DrawScores,
        replaceimg=None,
        mosaicsize=DO.MosaicSize)
    
    return newframe

def CallDeface(DO:DefaceOptions_t, MF:MediaFile_t, OutFilePath:str=""):
    global deface_thread
    DEBUG("FILE CONVERTING")
    callOptions = [MediaFile.FullPath]
    callOptions.extend(DO.generateOptionsStringArray())

    if(OutFilePath != ""):
        callOptions.append("--output")
        callOptions.append(OutFilePath)
    
    sysArgv_stored = sys.argv
    
    sys.argv = [sys.argv[0]]
    sys.argv.extend(callOptions)
    #deface_thread = threading.Thread(target = lambda:deface.main(), daemon=True) #don't overload editor thread
    deface.main()
    sys.arg = sysArgv_stored #recover original argv


    DEBUG("FILE CONVERTED")

##--------------------------------------------------------------------------------------------
##GUI EVENTS (COMMON CODE)

def UpdateDisplayedFrame_SameFrameNewParams(sameThreshold=False):
    global DefaceOptions
    global MediaFile
    if(MediaFile is None):
        return
    newFrame = AnonimizeFrame(MediaFile.CurrentFrameCache, DefaceOptions, True, DefaceOptions.dets_cache if sameThreshold else None)
    DisplayIioImage(newFrame)
    DEBUG("FrameUpdated")

def UpdateDisplayedFrame_NewFrame(frameNum:int):
    global MediaFile
    if(MediaFile is None):
        return
    MediaFile.UpdateCurrentFrame(frameNum)
    UpdateDisplayedFrame_SameFrameNewParams()
    DEBUG("FrameChanged")

def horizontalSlider_UpdateTextAndValues():
    global MainWindow
    global MediaFile
    global SEMAPHORE_spinBox_ScrollBar_Preview
    

    if(not SEMAPHORE_spinBox_ScrollBar_Preview):
        framenum=SlideBar2FrameNum(MediaFile)
        MainWindow.spinBox_Preview_Current_Frame.blockSignals(True)
        MainWindow.spinBox_Preview_Current_Frame.setValue(framenum)
        MainWindow.spinBox_Preview_Current_Frame.blockSignals(False)
    else:
        framenum = MainWindow.spinBox_Preview_Current_Frame.value()
        SEMAPHORE_spinBox_ScrollBar_Preview = False

    MainWindow.label_Preview_Current.setText(seconds_to_hhmmssmm(framenum2Seconds(framenum, MediaFile)))


#--------------------------------------------------------------------------------------------
##GUI EVENTS
def emulate_event_pushButtonLoadFile(filename):
    #Remember update warning and numpages
    global MainWindow
    global MediaFile
    global File_LastSelectedFolder_Load
    global ADMITTED_FILE_EXTENSIONS_PATTERN


    if(filename == ""):
        return
    
    filetype = mimetypes.guess_type(filename)[0]
    if(not (filetype.startswith("image") or filetype.startswith("video"))):
        print("File type not accepted")
        return

    MediaFile = MediaFile_t(filename)
    File_LastSelectedFolder_Load = MediaFile.Folder #remember folder
    MainWindow.lineEdit_OpenFile.setText(filename) #Write location up

    UpdateSlidebar(MediaFile)
    DisplayCurrentResolution(MediaFile.width, MediaFile.height)
    
    MainWindow.spinBox_NewResW.setValue(MediaFile.width)
    MainWindow.spinBox_NewResH.setValue(MediaFile.height)

    UpdateDisplayedFrame_NewFrame(MediaFile.CurrentFrameIndex)
    
    DEBUG("File_LastSelectedFolder_Load: " + File_LastSelectedFolder_Load)
    DEBUG("MediaFile.FullPath: " + MediaFile.FullPath)

    
def event_pushButtonLoadFile(): #Open PDF file
    #Remember update warning and numpages

    DEBUG("pushButtonLoad: pressed");
    fname = QFileDialog.getOpenFileName(None, 'Open file', "" ,ADMITTED_FILE_EXTENSIONS_PATTERN)

    filename = fname[0]
    
    DEBUG("fname:")
    DEBUG(fname)
    DEBUG(fname[0])

    emulate_event_pushButtonLoadFile(filename)


def event_pushButtonExport(): #Convert PDF with inserted pages and page reordering afterwards
    global MainWindow
    global MediaFile
    global DefaceOptions
    global File_LastSelectedFolder_Load
    global File_LastSelectedFolder_Save
    global ADMITTED_FILE_EXTENSIONS_PATTERN

    DEBUG("pushButtonConvert: pressed")
    if(MediaFile is None):
        print("ERROR: No file selected")
        return
    
    if(File_LastSelectedFolder_Save == ""):
        File_LastSelectedFolder_Save = File_LastSelectedFolder_Load

    fname = QFileDialog.getSaveFileName(None, "Export defaced media", os.path.join(File_LastSelectedFolder_Save, MediaFile.FileNameNoExt + "_anonymized" + MediaFile.Extension), ADMITTED_FILE_EXTENSIONS_PATTERN)
    OutFilePath = fname[0]
    File_LastSelectedFolder_Save = os.path.dirname(OutFilePath)

    CallDeface(DefaceOptions, MediaFile, OutFilePath)
    DEBUG("EXPORT FINISHED")


def event_pushButton_ResetValues():
    global DefaceOptions
    global MainWindow
    DefaceOptions.setDO(DefaceOptions_t())
    SetDefaceOptions(DefaceOptions)
    UpdateDisplayedFrame_SameFrameNewParams(False)



##----------

def event_checkBox_RemoveAudioTracks():
    global DefaceOptions
    global MainWindow
    DefaceOptions.RemoveAudioTracks = MainWindow.checkBox_RemoveAudioTracks.isChecked()
    UpdateDisplayedFrame_SameFrameNewParams(True)


def event_doubleSpinBox_DetThreshold(newValue):
    global DefaceOptions
    global MainWindow
    s:str=MainWindow.doubleSpinBox_DetThreshold.cleanText()
    if(len(s)<4 and not(len(s)>=3 and s[2] in "123456789") and not(len(s)>=2 and s[1] in "123456789") and not(len(s)>=1 and s[0] in "123456789")): #means the user is still writting, as not all four characters are displayed
        return

    if(MainWindow.doubleSpinBox_DetThreshold.value()<0.01):
        MainWindow.doubleSpinBox_DetThreshold.setValue(0.01) #if 0, program almost collapses, as any pixel is a face

    DefaceOptions.DetectionThreshold = MainWindow.doubleSpinBox_DetThreshold.value()
    UpdateDisplayedFrame_SameFrameNewParams(False)
    
def event_doubleSpinBox_BlurrSize(newValue):
    global DefaceOptions
    global MainWindow
    DefaceOptions.BlurrSize = MainWindow.doubleSpinBox_BlurrSize.value()
    UpdateDisplayedFrame_SameFrameNewParams(True)

##----------

def event_checkBox_Downscale():
    global DefaceOptions
    global MainWindow
    global centerface
    DefaceOptions.Downscale = MainWindow.checkBox_Downscale.isChecked()
    if(MainWindow.checkBox_Downscale.isChecked()):
        in_shape = DefaceOptions.DownscaleW, DefaceOptions.DownscaleH
        centerface = deface.CenterFace(in_shape=in_shape, backend='auto')
    else:
        centerface = deface.CenterFace(in_shape=None, backend='auto')
    UpdateDisplayedFrame_SameFrameNewParams(False)



def event_spinBox_NewRes_W(newValue):
    global DefaceOptions
    global MainWindow
    global centerface
    DefaceOptions.DownscaleW = MainWindow.spinBox_NewResW.value()
    if(MainWindow.checkBox_Downscale.isChecked()):
        in_shape = DefaceOptions.DownscaleW, DefaceOptions.DownscaleH
        centerface = deface.CenterFace(in_shape=in_shape, backend='auto')
        UpdateDisplayedFrame_SameFrameNewParams(False)


def event_spinBox_NewRes_H(newValue):
    global DefaceOptions
    global MainWindow
    global centerface
    DefaceOptions.DownscaleH = MainWindow.spinBox_NewResH.value()
    if(MainWindow.checkBox_Downscale.isChecked()):
        in_shape = DefaceOptions.DownscaleW, DefaceOptions.DownscaleH
        centerface = deface.CenterFace(in_shape=in_shape, backend='auto')
        UpdateDisplayedFrame_SameFrameNewParams(False)

    
##----------

def event_RadioButton_BlurrShape():
    global DefaceOptions
    global MainWindow

    BlurrShapeID:int = 0
    
    for i in range(len(RadioButtonCollection_BlurrShape)):
        if(RadioButtonCollection_BlurrShape[i].isChecked()):
            BlurrShapeID = i
            break

    DefaceOptions.BlurrShapeID = BlurrShapeID
    UpdateDisplayedFrame_SameFrameNewParams(True)
        

def event_RadioButton_BlurrMethod():
    global DefaceOptions
    global MainWindow
    
    BlurrMethodID:int = 0

    for i in range(len(RadioButtonCollection_BlurrMethod)):
        if(RadioButtonCollection_BlurrMethod[i].isChecked()):
            BlurrMethodID = i
            break

    DefaceOptions.BlurrMethodID = BlurrMethodID
    #MainWindow.spinBox_MosaicSize.setDisabled(not MainWindow.radioButton_BlurrMethod_Mosaic.isChecked())
    UpdateDisplayedFrame_SameFrameNewParams(True)


def event_spinBox_MosaicSize(newValue):
    global DefaceOptions
    global MainWindow
    DefaceOptions.MosaicSize = MainWindow.spinBox_MosaicSize.value()
    UpdateDisplayedFrame_SameFrameNewParams(True)

def event_horizontalSlider_Preview_whileMoving(value):
    global MainWindow
    global MediaFile
    DEBUG("MOVING")
    if(MediaFile is None):
        DEBUG("MediaFile is None")
        return
    if(MediaFile.IsImage):
        return
    
    horizontalSlider_UpdateTextAndValues()
    
    MediaFile.UpdateCurrentFrame(SlideBar2FrameNum(MediaFile))
    DisplayIioImage(MediaFile.CurrentFrameCache)
    #UpdateDisplayedFrame_NewFrame(SlideBar2FrameNum(MediaFile))
    

def event_horizontalSlider_Preview_afterMoving(value):
    global MainWindow
    global MediaFile
    DEBUG("MOVED")
    if(MediaFile is None):
        DEBUG("MediaFile is None")
        return
    horizontalSlider_UpdateTextAndValues()
    UpdateDisplayedFrame_NewFrame(SlideBar2FrameNum(MediaFile))
    
def event_spinBox_Preview_Current_Frame(value):
    global MainWindow
    global MediaFile
    global SEMAPHORE_spinBox_ScrollBar_Preview
    if(MediaFile is None):
        DEBUG("MediaFile is None")
        return
    if(MediaFile.IsImage):
        return
    SEMAPHORE_spinBox_ScrollBar_Preview =  True
    MainWindow.horizontalSlider_Preview.setValue(FrameNum2SlideBar(value, MediaFile))
    DEBUG("MOVED")

#---------------------------------------------------------------------------------------------

def Init():
    global MainWindow
    global RadioButtonCollection_BlurrShape
    global RadioButtonCollection_BlurrMethod
    global DefaceOptions
    global MediaFile

    #Precalculate global variables
    
    #Disable GUI elements
    MainWindow.pushButton_Export_2.setVisible(False)
    MainWindow.pushButton_Export_2.setDisabled(True)

    #Configure GUI elements
    MainWindow.horizontalSlider_Preview.setTracking(False)

    #Set events
    MainWindow.pushButton_LoadFile.clicked.connect(event_pushButtonLoadFile)

    MainWindow.pushButton_Export.clicked.connect(event_pushButtonExport)

    MainWindow.pushButton_ResetValues.clicked.connect(event_pushButton_ResetValues)


    MainWindow.checkBox_RemoveAudioTracks.clicked.connect(event_checkBox_RemoveAudioTracks)

    MainWindow.doubleSpinBox_DetThreshold.valueChanged.connect(event_doubleSpinBox_DetThreshold)
    MainWindow.doubleSpinBox_BlurrSize.valueChanged.connect(event_doubleSpinBox_BlurrSize)


    MainWindow.checkBox_Downscale.clicked.connect(event_checkBox_Downscale)

    MainWindow.spinBox_NewResW.valueChanged.connect(event_spinBox_NewRes_W)
    MainWindow.spinBox_NewResH.valueChanged.connect(event_spinBox_NewRes_H)

    for RB in RadioButtonCollection_BlurrShape:
        RB.clicked.connect(event_RadioButton_BlurrShape)

    for RB in RadioButtonCollection_BlurrMethod:
        RB.clicked.connect(event_RadioButton_BlurrMethod)
    
    MainWindow.spinBox_MosaicSize.valueChanged.connect(event_spinBox_MosaicSize)
    
    MainWindow.horizontalSlider_Preview.sliderMoved.connect(event_horizontalSlider_Preview_whileMoving)
    MainWindow.horizontalSlider_Preview.valueChanged.connect(event_horizontalSlider_Preview_afterMoving)

    MainWindow.spinBox_Preview_Current_Frame.valueChanged.connect(event_spinBox_Preview_Current_Frame)
    

    #TriggerEvents
    SetDefaceOptions(DefaceOptions) #Set default values to GUI
    event_RadioButton_BlurrMethod() #Disable mosaicsize if Mosaic option not selected

    ##Set LanguageID and correctly set all text

    DEBUG("GUI START")
    #OverloadStdout()
    #SHOW WINDOW
    #Test
    MainWindow.show()
    app.exec()
    DEBUG("PROGRAM ENDED")


#=============================================================================================

Init()