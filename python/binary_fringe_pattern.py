from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QSpinBox, QCheckBox
import sys
import cv2
import numpy as np
import math
import time
import threading

#from PyQt5.uic import loadUi
from interface import Ui_MainWindow
from binary_element import Element

class Window(QMainWindow, Ui_MainWindow):
    WIDTH = 640
    HEIGHT = 480
    FRAME_DELAY = 100
    WHT_INTENSITY = 255
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connectSignalsSlots()

        
    def connectSignalsSlots(self):

        self.ui.btnStart.clicked.connect(self.btnStartClicked)
        #self.action_Exit.triggered.connect(self.close)
        
    def btnStartClicked(self):
        freq_strg = self.ui.freqLineEdit.text()
        
        if freq_strg:
            freq_strglist = freq_strg.split(',')
            
        freq_array = [int (num) for num in freq_strglist]
        
        element = Element(self.ui.phsShftSpinBox.value(), freq_array, self.ui.horizontalChkkBox.isChecked(), self.ui.diag1ChkBox.isChecked(), self.ui.verticleChkBox.isChecked(), self.ui.diag2ChkBox.isChecked(), self.ui.spinBox.value())
        if element is not None:
            Window.loop(element)
        
    
    def loop(self):   
    # Parameter       
        #pattern_width = 640  # Width of the pattern
        #pattern_height = 480  # Height of the pattern
        num_patterns_param = self.num_phase_shift  # Number of sinusoidal patterns
        #frame_delay = 1  # Time delay between frames in milliseconds
        frequency_list = self.freq_list # Frequency list of sinusoidal pattern
        #white_intensity =255 #0-255
        angle_degrees_param = self.slanted_angle

        # Create a window for displaying the pattern
        cv2.namedWindow("Sinusoidal Pattern", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Sinusoidal Pattern", Window.WIDTH, Window.HEIGHT)

        # Main loop
        #window()
        while True:
            for i in range(len(frequency_list)):
                freq_param =frequency_list[i]
                if(self.horizontal):
                    Window.horizontal(freq_param, num_patterns_param)
                #sleep()
                if(self.slant1):
                    Window.slant(freq_param, num_patterns_param, angle_degrees_param)
                #sleep()
                if(self.verticle):
                    Window.vertical(freq_param, num_patterns_param)
                #sleep()
                if(self.slant2):
                    Window.slant2(freq_param, num_patterns_param, angle_degrees_param)
                #sleep()
           
             #Break the loop if the user presses the "Esc" key
            if cv2.waitKey(1) == 27 | self.clos:
                break

        # Close the window
        cv2.destroyAllWindows()
    
    def horizontal(freq, num_patterns):
        for i in range(num_patterns):  
            phase_shift = (2 * math.pi * i) / num_patterns
            pattern_x = np.zeros((Window.HEIGHT, Window.WIDTH), dtype=np.uint8)
        
            for y in range(Window.HEIGHT):
                for x in range(Window.WIDTH):
                    intensity = Window.WHT_INTENSITY * (0.5 + 0.5 * math.sin(2 * math.pi * freq * x / Window.WIDTH + phase_shift))
                    pattern_x[y, x] = int(intensity)
        
            cv2.imshow("Sinusoidal Pattern", pattern_x)
            cv2.waitKey(Window.FRAME_DELAY) 
    
    def vertical(freq, num_patterns):
        for i in range(num_patterns):  
            phase_shift = (2 * math.pi * i) / num_patterns
            pattern_y = np.zeros((Window.HEIGHT, Window.WIDTH), dtype=np.uint8)
        
            for y in range(Window.HEIGHT):
                for x in range(Window.WIDTH):
                    intensity = Window.WHT_INTENSITY * (0.5 + 0.5 * math.sin(2 * math.pi * freq * y / Window.HEIGHT + phase_shift))
                    pattern_y[y, x] = int(intensity)
        
            cv2.imshow("Sinusoidal Pattern", pattern_y)
            cv2.waitKey(Window.FRAME_DELAY)   
        
    def slant2(freq, num_patterns, angle_degrees):
        for i in range(num_patterns):
            phase_shift = (2 * math.pi * i) / num_patterns
            angle_radians = math.radians(angle_degrees)
            pattern_diag = np.zeros((Window.HEIGHT, Window.WIDTH), dtype=np.uint8)
        
            for y in range(Window.HEIGHT):
                for x in range(Window.WIDTH):
                    intensity = Window.WHT_INTENSITY * (0.5 + 0.5 * math.sin(2 * math.pi * freq * (x * math.cos(angle_radians) + y * math.sin(angle_radians)) / (Window.WIDTH + Window.HEIGHT) + phase_shift))
                    pattern_diag[y, x] = int(intensity)
        
            cv2.imshow("Sinusoidal Pattern", pattern_diag)
            cv2.waitKey(Window.FRAME_DELAY)
        
    def slant(freq, num_patterns, angle_degrees):
        for i in range(num_patterns):
            phase_shift = (2 * math.pi * i) / num_patterns
            angle_radians = math.radians(angle_degrees)
            pattern_diag = np.zeros((Window.HEIGHT, Window.WIDTH), dtype=np.uint8)
        
            for y in range(Window.HEIGHT):
                for x in range(Window.WIDTH):
                    intensity = Window.WHT_INTENSITY * (0.5 + 0.5 * math.sin(2 * math.pi * freq * (x * math.cos(angle_radians) - y * math.sin(angle_radians)) / (Window.WIDTH + Window.HEIGHT) + phase_shift))
                    pattern_diag[y, x] = int(intensity)
        
            cv2.imshow("Sinusoidal Pattern", pattern_diag)
            cv2.waitKey(Window.FRAME_DELAY)
        
    def sleep():
        time.sleep(4)

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

