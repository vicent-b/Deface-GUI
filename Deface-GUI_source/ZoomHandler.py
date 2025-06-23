#Credits (mostly) to chatGPT on this one


from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsTextItem
from PySide6.QtCore import Qt, QObject
from PySide6.QtGui import QTransform, QWheelEvent, QColor
import sys

# This object will handle zooming via an event filter
class ZoomHandler(QObject):
    def __init__(self, view:QGraphicsView, zoom_factor_step:float = 1.15, minimum_scale:float=None):
        super().__init__(view)
        self.view:QGraphicsView = view
        self.zoom_factor_step:float = zoom_factor_step    # Factor to zoom in/out per wheel event

        self.minimum_scale:float = minimum_scale if minimum_scale is not None else view.transform().m11() #Assume image is configured to already fit in frame. Asume x zoom (m11) is equal to y zoom (m22)
        self.current_zoom:float = minimum_scale if minimum_scale is not None else 1.0                     # Tracks the current zoom level
        self.enabled:bool = False
        self.already_connected:bool = False

    #Redefines characteristics when image changes 
    def reset(self, view:QGraphicsView, zoom_factor_step:float = 1.15, minimum_scale:float=None, enabled:bool=False, already_connected:bool = None):
        self.view:QGraphicsView = view
        self.zoom_factor_step:float = zoom_factor_step    # Factor to zoom in/out per wheel event

        self.minimum_scale:float = minimum_scale if minimum_scale is not None else view.transform().m11() #Assume image is configured to already fit in frame. Asume x zoom (m11) is equal to y zoom (m22)
        self.current_zoom:float = minimum_scale if minimum_scale is not None else 1.0                     # Tracks the current zoom level
        self.enabled:bool = enabled
        self.already_connected:bool = already_connected if already_connected is not None else self.already_connected #if it connects as event every time image changes , it may add a lot of processing overhead


    def eventFilter(self, obj, event):
        # Handle only wheel events
        if self.enabled and event.type() == event.Type.Wheel and isinstance(event, QWheelEvent):
            # Optional: Only zoom when Ctrl is held (like many editors)
            if event.modifiers() & Qt.ControlModifier:

                # Get the mouse position in scene coordinates before zooming
                old_scene_pos = self.view.mapToScene(event.position().toPoint())

                # Adjust zoom level
                if event.angleDelta().y() > 0:
                    self.current_zoom *= self.zoom_factor_step
                else:
                    self.current_zoom /= self.zoom_factor_step
                
                self.current_zoom = max(self.current_zoom , self.minimum_scale)

                # Set the new transform (absolute, not relative)
                transform = QTransform()
                transform.scale(self.current_zoom, self.current_zoom)
                self.view.setTransform(transform)

                # Get the new scene position after applying zoom
                new_scene_pos = self.view.mapToScene(event.position().toPoint())

                # Calculate the difference between old and new position to keep the view centered on mouse
                offset = new_scene_pos - old_scene_pos
                self.view.translate(offset.x(), offset.y())  # Scroll view to preserve cursor focus

                return True  # We've handled the event
            
        # Handle double-click event for fitInView
        if self.enabled and event.type() == event.Type.MouseButtonDblClick:
            if event.button() == Qt.LeftButton:
                # Reset zoom by fitting the entire scene in the view
                self.view.fitInView(self.view.sceneRect(), Qt.KeepAspectRatio)
                self.current_zoom = self.view.transform().m11()  # Update current_zoom
                return True

        return False  # Pass through other events


    def engage(self):
        self.enabled = True

        # Set anchor policies to ensure zoom is mouse-aware
        self.view.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.view.setResizeAnchor(QGraphicsView.ViewportAnchor.NoAnchor)

        if(self.already_connected):
            return
        
        self.already_connected = True
        self.view.viewport().installEventFilter(self)
    
    def setEnabled(self, enabled:bool):
        self.enabled = enabled

        

