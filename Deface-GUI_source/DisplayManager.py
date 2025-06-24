from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from ZoomHandler import *
import numpy as np

class DisplayManager():

    def __init__(self, view:QGraphicsView, useOpenGL:bool = False): #OpenGL is False as default, as ZoomHandler breaks
        self.view:QGraphicsview = view
        self.zoom_handler:ZoomHandler = ZoomHandler(view)
        self.zoom_handler.engage() #.reset() will be called later

        self.scene_cache:QGraphicsScene = None
        self.pixmapItem_cache:QPixmap   = None

        if(useOpenGL):
            try:
                view.setViewport(QOpenGLWidget())
                print("Open GL used successfully")
            except:
                print("Error: Open GL could not be used to optimize display")


    def ImageIO_to_QImage(self, image):
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


    def DisplayQImage(self, qimage, image_size_changed:bool = True):
        self.view.setUpdatesEnabled(False)

        pixmap = QPixmap.fromImage(qimage)

        self.view.setSceneRect(0,0,pixmap.width(), pixmap.height())

        #reuse old QGraphicsScene if same size
        if(self.scene_cache is None or image_size_changed):
            self.scene_cache = QGraphicsScene()
            self.scene_cache.setSceneRect(self.view.sceneRect())
        else:
            self.scene_cache.clear() #clear all items
        
        #reuse old QPixmapItem if same size
        if(self.pixmapItem_cache is not None or image_size_changed): #Not sure if second part is necessary    
            self.pixmapItem_cache = QGraphicsPixmapItem()
            self.pixmapItem_cache.setPos(0, 0)
        
        self.pixmapItem_cache.setPixmap(pixmap)


        self.scene_cache.addItem(self.pixmapItem_cache)
        self.view.setScene(self.scene_cache)

        if(image_size_changed):
            self.view.fitInView(self.pixmapItem_cache, Qt.KeepAspectRatio) #Fullscreen it
            self.zoom_handler.reset(self.view) #Reset zoom handler to new image
            self.zoom_handler.setEnabled(True)
        
        self.view.setUpdatesEnabled(True)
        #self.view.update() #does not seem necessary. Updates anyway


    def DisplayIioImage(self, iioimage, image_size_changed:bool = True):
        qimage = self.ImageIO_to_QImage(iioimage)
        self.DisplayQImage(qimage, image_size_changed)


    def DisplayTextImage(self, text_HTML:str, textColor:QColor = QColor(160,160,160)):

        screenText = QGraphicsTextItem()
        screenText.setHtml(text_HTML)
        screenText.adjustSize() #requiered for it to have an alignment if requested
        screenText.setDefaultTextColor(textColor)
        screenText_Scene = QGraphicsScene()

        self.view.setSceneRect(screenText.boundingRect())
        screenText_Scene.setSceneRect(self.view.sceneRect())
        screenText_Scene.addItem(screenText)
        self.view.setScene(screenText_Scene)
        self.view.fitInView(screenText, Qt.KeepAspectRatio)

        self.zoom_handler.reset(self.view)
        self.zoom_handler.setEnabled(True)