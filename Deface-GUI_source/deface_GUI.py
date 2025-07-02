import os
import sys
from enum import Enum
import math
import datetime
import av
import imageio.v2 as iio
#import Lib.deface as deface #important to import as just deface, otherwise recursive calls within the package fail
#import deface.deface as deface
from deface import deface as deface
import QueueStreams as QS
import mimetypes

from Mainwindow import *
from DisplayManager import *



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


class Worker(QThread):

    def __init__(self, fcn, finish_fcn=None):
        super().__init__()
        self.LocalVarDictionary={} # LocalVarDictionary['myvariablename']=Value is used both to create and edit existing variables
        self.fcn = fcn
        self.finish_fcn = finish_fcn

        if(self.finish_fcn is not None): #DO NOT USE MOVETOTHREAD OR WILL EXECUTE EVENT IN THE PARALELL THREAD OF RUN()
            self.finished.connect(lambda: finish_fcn(self.LocalVarDictionary))
    
    def run(self) -> None:
        self.fcn(self.LocalVarDictionary)
    


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
    
    def set(self, DetectionThreshold:float = 0.2, BlurrSize:float = 1.3, RemoveAudioTracks:bool = False, Downscale:bool = False, DownscaleW:int = 1, DownscaleH:int = 1, BlurrShapeID:int = BlurrShape_t.ELLIPSE.value, BlurrMethodID:int = BlurrMethod_t.BLURR.value, MosaicSize:int=20) -> None:
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
    
    def setDO(self, DO) -> None:
        self.set(DO.DetectionThreshold, DO.BlurrSize, DO.RemoveAudioTracks, DO.Downscale, DO.DownscaleW, DO.DownscaleH, DO.BlurrShapeID, DO.BlurrMethodID, DO.MosaicSize)

        DEBUG("DO_SET")

    def generateOptionsStringArray(self) -> list[str]:
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
    
    def generateOptionsString(self) -> str:
        varArray=self.generateOptionsStringArray()
        varString:str=""

        for s in varArray:
            varString = varString + " "+"\""+s+"\""
        
        return varString



class MediaFile_t:
    def __init__(self, FullPath:str):
        self.FullPath:str = FullPath
        self.FileName:str = os.path.basename(FullPath)
        self.Folder:str = os.path.dirname(FullPath)
        self.FileNameNoExt:str=""
        self.Extension:str =""
        self.FileNameNoExt, self.Extension = os.path.splitext(self.FileName)
        filetype=mimetypes.guess_type(FullPath)[0]
        self.IsImage:bool = (filetype.startswith("image"))

        self.durationSeconds:float|None = 0
        self.NFrames:int = 0
        self.framerate:float|None = 0

        self.width:int  = 0
        self.height:int = 0
        self.channels:int = 0

        self.iioHandler = None

        self.estimatedUncompressedSizeBytes:int = 0

        self.FrameCaches = [None, None] #Primary (fixed) and secondary (temporary) framecaches 



        video_container = av.open(FullPath)
        video_stream=next(s for s in video_container.streams if s.type == 'video')
        self.durationSeconds = float(video_stream.duration * video_stream.time_base) if video_stream is not None and video_stream.duration is not None else None
        
        aproxNFrames:int = video_stream.frames
        if (aproxNFrames == 0 and video_stream.average_rate is not None):
            aproxNFrames == self.durationSeconds*video_stream.average_rate
        video_container.close()

        
        self.iioHandler = self.get_new_iioHandler()
        

        #DEPRECATED: Only useful for files that support random access to frames. This is not usuallythe case, this is why it has been substituted by loading the hole file onto RAM
        #if(aproxNFrames is None or aproxNFrames == 0):
        #    self.NFrames:int = self.CountExactFrames(6)
        #else:
        #    self.NFrames:int = self.CountExactFrames(math.floor(math.log(aproxNFrames, 5)))
        

        self.NFrames = self.countExactFramesSequential(aproxNFrames)
        

        DEBUG(self.NFrames)

        self.framerate = self.NFrames/self.durationSeconds if self.durationSeconds is not None else None
        self.CurrentFrameIndex:int = 0 
        #self.CurrentFrameCache = self.iioHandler.read(index=0)
        #self.CurrentFrameCache = self.iioHandler.read(index=self.CurrentFrameIndex)
        self.CurrentFrameCache = self.getFrame(self.CurrentFrameIndex)
        DEBUG(self.CurrentFrameIndex)
        


        probeimage=self.CurrentFrameCache
        if(probeimage.ndim == 2):
            self.height, self.width = probeimage.shape
            self.channels = 1
        elif (probeimage.ndim == 3):
            self.height, self.width, self.channels = probeimage.shape
        
        self.estimatedUncompressedSizeBytes = self.width * self.height * self.channels * probeimage.dtype.itemsize * self.NFrames
        print("Estimated uncompressed size: "+str(self.estimatedUncompressedSizeBytes/1024.0/1024.0/1024.0) + " GB")


       

    def __del__(self):
        self.iioHandler.close()
        self.resetFrameCaches()
        DEBUG("Old IIO Deleted")


    def get_new_iioHandler(self):
        if not self.IsImage:
            local_iioHandler = iio.imopen(self.FullPath, "r", plugin="pyav")
        else:
            local_iioHandler = iio.imopen(self.FullPath, "r")
        
        return local_iioHandler

    def resetFrameCache(self, cacheIndex:int) -> None:
        self.FrameCaches[cacheIndex] = None

    def resetFrameCaches(self) -> None:
        for i in range(len(self.FrameCaches)):
            self.resetFrameCache(i)

    def cacheFrame(self, cacheIndex:int, index:int, frameData=None) -> None:
        
        if (self.FrameCaches[cacheIndex] is None):
            self.FrameCaches[cacheIndex] = [None]*self.NFrames
        
        if (self.FrameCaches[cacheIndex][index] is None):
            if (frameData is None):
                self.FrameCaches[index] = self.iioHandler.read(index = index)
            else:
                self.FrameCaches[index] = frameData

    def cacheFrames(self, cacheIndex:int, indexArr) -> None:
        for i in indexArr:
            self.cacheFrame(cacheIndex, i)

    def cacheFramesLargeArr(self, cacheIndex, indexArr, progressfcn_j_tot_f_tot_stage = None) -> None:

        fcn = progressfcn_j_tot_f_tot_stage

        if (self.FrameCaches[cacheIndex] is None):
            self.FrameCaches[cacheIndex] = [None]*self.NFrames

        if(fcn is not None):
            fcn(0, len(indexArr), 0, self.NFrames, 0)
        

        local_iioHandler = self.get_new_iioHandler()

        framenum = 0
        j = 0 # using j is much more efficient than "in indexArr"
        for frame in local_iioHandler.iter():
            if (j >= len(indexArr)):
                break

            if(framenum == indexArr[j]):

                if(fcn is not None):
                    fcn(j, len(indexArr), framenum, self.NFrames, 1)

                if(self.FrameCaches[cacheIndex][framenum] is None):
                    self.FrameCaches[cacheIndex][framenum] = frame

                j=j+1
            
            framenum=framenum+1

        local_iioHandler.close()

        if(fcn is not None):
            fcn(j-1, len(indexArr), indexArr[j-1], self.NFrames, 2)
    


    def getFrame(self, index:int, cacheFrame:bool = False, cacheIndex:int = 2):

        f = None
        foundInCache:bool = False

        for i in range(len(self.FrameCaches)):
            if(self.FrameCaches[i] is not None):
                f=self.FrameCaches[i][index]
                foundInCache = True if f is not None else False

        if(f is None):
            f = self.iioHandler.read(index=index)
        
        if(cacheFrame and not foundInCache):
            self.cacheFrame(cacheIndex, index, f)
        
        return f




    def UpdateCurrentFrame(self, frameNum:int) -> None:
        frameNum = frameNum if (frameNum < self.NFrames) else self.NFrames
        if(frameNum == self.CurrentFrameIndex):
            return
        self.CurrentFrameIndex = frameNum
        #self.CurrentFrameCache = self.iioHandler.read(index=self.CurrentFrameIndex)
        self.CurrentFrameCache = self.getFrame(self.CurrentFrameIndex)

        
    def currentTimeSeconds(self) -> float:
        return float(self.CurrentFrameIndex*self.durationSeconds/self.NFrames) if self.durationSeconds is not None else None
    
    def countExactFrames(self, digitPower:int=0, base:int=0) -> int:
        #Only useful for files that support random access. Usually, this isn't the case.
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
                    return self.countExactFrames(digitPower-1,idx_old)
            
    def countExactFramesSequential(self, aproxNFrames:int|None) -> int:

        aproxNFramesStr:str = str(aproxNFrames) if aproxNFrames is not None and aproxNFrames > 0 else "???"
        sys.stdout.write("\n")

        local_iioHandler = self.get_new_iioHandler()

        i=0
        for frame in local_iioHandler.iter():
            i=i+1
            if(i==1 or i%10==0):
                sys.stdout.write("\r COUNTING FRAMES: "+str(i)+" / "+aproxNFramesStr)

        sys.stdout.write("\r COUNTING FRAMES: "+str(i)+" / "+str(i)+"\n")

        local_iioHandler.close()

        return i


##GLOBAL VARS

DefaceOptions:DefaceOptions_t = DefaceOptions_t()
MediaFile:MediaFile_t|None = None

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

Displayer = DisplayManager(MainWindow.graphicsView_Preview)

#thread coordination
SEMAPHORE_spinBox_ScrollBar_Preview:bool = False #When frame number is edited, slider value is changed. When slider moves, new frame number is displayed on spingbox. This semaphore ensures spinbox frame number is not edited over again when slider position is set (as slidebar precision is worse than that of the spinbox) by blocking part of the code in horizontalSlider_UpdateTextAndValues()

stdout_emitter:QS.streamEmitter|None = None
stdout_receiver:QS.streamReceiver|None = None
stdout_thread = None

loadfile_thread:Worker|None = None

deface_thread:Worker|None = None #Execute deface tool in a paralell thread

#Consts
ADMITTED_FILE_EXTENSIONS_PATTERN = "Video (*.mov *.avo *.mpg *.mp4 *.mkv *.wmv);;Common images (*.jpg *.jpeg *.png *.tiff *.bmp);;Any files (*)"

#--------------------------------------------------------------------------------------------
##BASIC UTIL FUNCTIONS

def framenum2Seconds(NFrame, MF:MediaFile_t) -> float:
    return float(NFrame)/float(MF.NFrames-1)*MF.durationSeconds

def seconds_to_hhmmssmm(sec:float) -> str:
    return str(datetime.timedelta(seconds=sec))


#--------------------------------------------------------------------------------------------
##BASIC GUI FUNCTIONS

def ManipulateStdoutQueue(queueElement) -> None:
    global MainWindow
    s=queueElement[0]
    #MainWindow.textEdit_ConsoleOutput.append(s)
    MainWindow.textEdit_ConsoleOutput.moveCursor (QTextCursor.End)
    MainWindow.textEdit_ConsoleOutput.insertPlainText (s)
    MainWindow.textEdit_ConsoleOutput.moveCursor (QTextCursor.End)


def OverloadStdout() -> None:
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


def ReadDefaceOptions(DO: DefaceOptions_t) -> None:
    
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

    
    
def SetDefaceOptions(DO: DefaceOptions_t) -> None:
    MainWindow.doubleSpinBox_DetThreshold.setValue(DO.DetectionThreshold)
    MainWindow.doubleSpinBox_BlurrSize.setValue(DO.BlurrSize)
    MainWindow.checkBox_RemoveAudioTracks.setChecked(DO.RemoveAudioTracks)
    MainWindow.checkBox_Downscale.setChecked(DO.Downscale)
    MainWindow.spinBox_NewResW.setValue(DO.DownscaleW)
    MainWindow.spinBox_NewResH.setValue(DO.DownscaleH)
    RadioButtonCollection_BlurrShape[DO.BlurrShapeID].setChecked(True)
    RadioButtonCollection_BlurrMethod[DO.BlurrMethodID].setChecked(True)
    MainWindow.spinBox_MosaicSize.setValue(DO.MosaicSize)
    

def SlideBar2FrameNum(MF:MediaFile_t, Slidebar=MainWindow.horizontalSlider_Preview) -> int:
    Pos=Slidebar.sliderPosition()
    value=float(Pos-Slidebar.minimum())/float(Slidebar.maximum()-Slidebar.minimum())
    return round(value*(MF.NFrames-1))

def FrameNum2SlideBar(FrameNum:int, MF:MediaFile_t, Slidebar=MainWindow.horizontalSlider_Preview) -> int:
    value = float(FrameNum)/float(MF.NFrames-1)
    return round(value*(Slidebar.maximum()-Slidebar.minimum())+Slidebar.minimum())

def UpdateSlidebar(MF: MediaFile_t) -> None:
    global MainWindow
    
    if(MF.IsImage):
        MainWindow.label_Preview_End.setText("ff:ff:ff")
        MainWindow.label_Preview_End_Frame.setText(str(MF.NFrames-1))

        MainWindow.horizontalSlider_Preview.setValue(0)      #not needed really
        MainWindow.horizontalSlider_Preview.setMinimum(0)
        MainWindow.horizontalSlider_Preview.setMaximum(1000) #default


        MainWindow.label_Preview_Current.setText("xx:xx:xx")

    else: #if is video

        MainWindow.label_Preview_End.setText(seconds_to_hhmmssmm(MF.durationSeconds))
        MainWindow.label_Preview_End_Frame.setText(str(MF.NFrames-1))
    
        MainWindow.horizontalSlider_Preview.setValue(0)       #not needed really
        MainWindow.horizontalSlider_Preview.setMinimum(0)
        MainWindow.horizontalSlider_Preview.setMaximum(math.floor(MF.durationSeconds*2))
        
        MainWindow.label_Preview_Current.setText(seconds_to_hhmmssmm(framenum2Seconds(MF.CurrentFrameIndex, MF)))

    MainWindow.spinBox_Preview_Current_Frame.setValue(MF.CurrentFrameIndex)
    MainWindow.spinBox_Preview_Current_Frame.setMaximum(MF.NFrames-1)

    DEBUG("SlidebarUpdated")   



def DisplayCurrentResolution(W:int,H:int) -> None:
    global MainWindow
    MainWindow.lineEdit_OriginalRes.setText(str(W)+" x "+str(H))


#--------------------------------------------------------------------------------------------
##COMPLEX FUNCTIONS

def GenerateNewMediaFile(filename:str) -> MediaFile_t:

    MF = MediaFile_t(filename)
    
    #Display caching progress
    def progressfcn_j_tot_f_tot_stage(j, jtot, f, ftot, stage):
        if (stage == 0):
            sys.stdout.write("\n")
        if (stage == 1):
            sys.stdout.write("\rLOADING FRAME Nº "+str(f)+" / "+str(ftot-1)+": "+str(j)+" of "+str(jtot-1))
        if (stage == 2):
            sys.stdout.write("\n")


    MAX_GB = 2.0
    if (not MF.IsImage):
        if (MF.estimatedUncompressedSizeBytes/(1024.0**3) <= MAX_GB):
            print("Size small enough (<="+str(MAX_GB)+"GB). Caching whole file in memory")
            MF.cacheFramesLargeArr(0, list(range(MF.NFrames)), progressfcn_j_tot_f_tot_stage)
            
        elif (MF.estimatedUncompressedSizeBytes/(1024.0**3)/(MF.framerate/2.0) < MAX_GB): #2 is the slidebar steps per second
            print("Medium file size. Caching in memory only frames that match slidebar. Expected size:" +str(MF.estimatedUncompressedSizeBytes/(1024.0**3)/(MF.framerate/2.0))+ " GB")
            #Caculated in same way as in UpdateSlidebar()
            max_slidebar = math.floor(MF.durationSeconds*2)
            indexes=list(range(max_slidebar+1))
            for i in range(len(indexes)):
                Pos= indexes[i]
                value=float(Pos)/float(max_slidebar)
                indexes[i] = round(value*(MF.NFrames-1))
            MF.cacheFramesLargeArr(0, indexes, progressfcn_j_tot_f_tot_stage)
        else:
            print("File too big. No initial chaching done")
    
    return MF


def AfterGenerateNewMediaFile(MF:MediaFile_t) -> None:
    global MainWindow
    global File_LastSelectedFolder_Load

    File_LastSelectedFolder_Load = MF.Folder #remember folder
    MainWindow.lineEdit_OpenFile.setText(MF.FullPath) #Write location up

    UpdateSlidebar(MediaFile)
    DisplayCurrentResolution(MF.width, MF.height)
    
    MainWindow.spinBox_NewResW.setValue(MF.width)
    MainWindow.spinBox_NewResH.setValue(MF.height)

    UpdateDisplayedFrame_NewFrameNewFile(MF.CurrentFrameIndex)
    
    DEBUG("File_LastSelectedFolder_Load: " + File_LastSelectedFolder_Load)
    DEBUG("MediaFile.FullPath: " + MF.FullPath)


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

def CallDeface(DO:DefaceOptions_t, MF:MediaFile_t, OutFilePath:str="") -> None:
    global deface_thread
    DEBUG("FILE CONVERTING")
    
    """
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
    """
    #Previous method had unresolved bug: after processing a video, another video could not be opened
    defacecall = "deface " + " \""+MediaFile.FullPath+"\" " + DO.generateOptionsString()
    if(OutFilePath != ""):
        defacecall = defacecall + " --output "+" \""+OutFilePath+"\" "
    
    print(">> "+defacecall)
    os.system(defacecall)

    DEBUG("FILE CONVERTED")


def Threaded_CallDeface(DO:DefaceOptions_t, MF:MediaFile_t, OutFilePath:str="") -> None:
    global deface_thread
    if(deface_thread is not None and deface_thread.isRunning() and not deface_thread.isFinished()):
        print("\nPlease, wait for Deface to finish processing the previous file")
        return

    thread_fcn = lambda LocalVarDictionary: CallDeface(DO, MF, OutFilePath)
    deface_thread = Worker(thread_fcn) #don't overload editor thread
    deface_thread.start()
    DEBUG("DEFACE THREAD STARTED")


##--------------------------------------------------------------------------------------------
##GUI EVENTS (COMMON CODE)

def UpdateDisplayedFrame_SameFrameNewParams(sameThreshold:bool=False) -> None:
    global DefaceOptions
    global MediaFile
    global Displayer
    if(MediaFile is None):
        return
    newFrame = AnonimizeFrame(MediaFile.CurrentFrameCache, DefaceOptions, True, DefaceOptions.dets_cache if sameThreshold else None)
    Displayer.DisplayIioImage(newFrame, False)
    DEBUG("FrameUpdated")

def UpdateDisplayedFrame_NewFrameSameFile(frameNum:int) -> None:
    global MediaFile
    global Displayer
    if(MediaFile is None):
        return
    MediaFile.UpdateCurrentFrame(frameNum)
    newFrame = AnonimizeFrame(MediaFile.CurrentFrameCache, DefaceOptions, True, None)
    Displayer.DisplayIioImage(newFrame, False)
    DEBUG("FrameChanged")

def UpdateDisplayedFrame_NewFrameNewFile(frameNum:int) -> None:
    global MediaFile
    global Displayer
    if(MediaFile is None):
        return
    MediaFile.UpdateCurrentFrame(frameNum)
    newFrame = AnonimizeFrame(MediaFile.CurrentFrameCache, DefaceOptions, True, None)
    Displayer.DisplayIioImage(newFrame, True)
    DEBUG("File and frame changed")

def horizontalSlider_UpdateTextAndValues() -> None:
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
def emulate_event_pushButtonLoadFile(filename:str) -> None:
    #Remember update warning and numpages
    global MediaFile
    global loadfile_thread

    if(filename == ""):
        return
    
    filetype = mimetypes.guess_type(filename)[0]
    if(not (filetype.startswith("image") or filetype.startswith("video"))):
        print("File type not accepted")
        return



    #MediaFile = GenerateNewMediaFile(filename)
    #AfterGenerateNewMediaFile(MediaFile)

    def LoadThread(LocalVarDictionary):
        LocalVarDictionary['MediaFile_paralell'] = GenerateNewMediaFile(filename)

    def WhenLoadThreadFinished(LocalVarDictionary):
        global MediaFile
        MediaFile = LocalVarDictionary['MediaFile_paralell']
        AfterGenerateNewMediaFile(MediaFile)

    loadfile_thread = Worker(LoadThread, WhenLoadThreadFinished)
    loadfile_thread.start()




    
def event_pushButtonLoadFile():
    global loadfile_thread
    global ADMITTED_FILE_EXTENSIONS_PATTERN 
    #Remember update warning and numpages

    DEBUG("pushButtonLoad: pressed")
    if(loadfile_thread is not None and loadfile_thread.isRunning() and not loadfile_thread.isFinished()):
        print("\nPlease, wait for file to finish loading")
        return
    fname = QFileDialog.getOpenFileName(None, 'Open file', "" ,ADMITTED_FILE_EXTENSIONS_PATTERN)

    filename = fname[0]
    
    DEBUG("fname:")
    DEBUG(fname)
    DEBUG(fname[0])

    emulate_event_pushButtonLoadFile(filename)


def event_pushButtonExport():
    global deface_thread
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
    
    if(deface_thread is not None and deface_thread.isRunning() and not deface_thread.isFinished()):
        print("\nPlease, wait for Deface to finish processing the previous file")
        return
    
    if(File_LastSelectedFolder_Save == ""):
        File_LastSelectedFolder_Save = File_LastSelectedFolder_Load

    fname = QFileDialog.getSaveFileName(None, "Export defaced media", os.path.join(File_LastSelectedFolder_Save, MediaFile.FileNameNoExt + "_anonymized" + MediaFile.Extension), ADMITTED_FILE_EXTENSIONS_PATTERN)
    OutFilePath = fname[0]
    File_LastSelectedFolder_Save = os.path.dirname(OutFilePath)

    Threaded_CallDeface(DefaceOptions, MediaFile, OutFilePath)
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
    global Displayer
    DEBUG("MOVING")
    if(MediaFile is None):
        DEBUG("MediaFile is None")
        return
    if(MediaFile.IsImage):
        return
    
    horizontalSlider_UpdateTextAndValues()
    
    MediaFile.UpdateCurrentFrame(SlideBar2FrameNum(MediaFile))
    Displayer.DisplayIioImage(MediaFile.CurrentFrameCache, False)
    #UpdateDisplayedFrame_NewFrameSameFile(SlideBar2FrameNum(MediaFile)) #lines above display new frame without processing it for deface, as processing it while moving creates lag
    

def event_horizontalSlider_Preview_afterMoving(value):
    global MainWindow
    global MediaFile
    DEBUG("MOVED")
    if(MediaFile is None):
        DEBUG("MediaFile is None")
        return
    if(MediaFile.IsImage):
        return
    horizontalSlider_UpdateTextAndValues()
    UpdateDisplayedFrame_NewFrameSameFile(SlideBar2FrameNum(MediaFile))
    
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

def Init() -> None:
    global deface_thread
    global MainWindow
    global RadioButtonCollection_BlurrShape
    global RadioButtonCollection_BlurrMethod
    global DefaceOptions
    global MediaFile
    global Displayer

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

    #Set default image view
    Displayer.DisplayTextImage("""
    <div align="center">
      <p>Use Control + mouse wheel for zooming</p>
      <p>Double click left to reset zoom</p>
    </div>
    """)

    app.exec()

    if (deface_thread is not None):
        deface_thread.wait()

    DEBUG("PROGRAM ENDED")



#=============================================================================================

if __name__ == '__main__':
    Init()