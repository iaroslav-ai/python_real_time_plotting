'''
contains convenient class for high performance plotting
'''

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import threading
import time

class series:
    def __init__(self, x, y, name="", color = "r"):
        self.x = x;
        self.y = y;
        self.name = name;
        self.color = color;
        self.curve = []

class subplot:
    def __init__(self, name = ""):
        self.sequences = [];
        self.name = name;
        self.p = []
        
    def add(self, sequence):
        self.sequences.append(sequence)

class plot:
    
    def __init__(self, columns = 5, name = "", update_every=50):
        self.columns = columns;
        self.name = name;
        self.subplots = []
        self.upate_every = update_every;
    
    def add(self, sub):
        self.subplots.append(sub)
    
    def compile(self):
        global slf;
        slf = self;
                        
        def runthr(): 
            global slf;
            
            app = QtGui.QApplication([])
            win = pg.GraphicsWindow(title=slf.name)
            win.setWindowTitle(slf.name)
            
            # Enable antialiasing for prettier plots
            pg.setConfigOptions(antialias=True)
            
            # create necessary window elements
            idx = 1;
            for sub in slf.subplots:
                sub.p = win.addPlot(title=sub.name)
                
                for seq in sub.sequences:
                    curve = sub.p.plot(pen=seq.color)
                    seq.curve = curve;
                
                if idx % slf.columns == 0:
                    win.nextRow();
                    
                idx = idx + 1
            
            def update():
                global slf;
                
                for sub in slf.subplots: 
                    
                    if sub.p == []:
                        continue;
                                       
                    for seq in sub.sequences:     
                        if seq.curve == []:
                            continue;              
                        seq.curve.setData(seq.y)
                        
                    sub.p.enableAutoRange('xy', False)
            
            timer = QtCore.QTimer()
            timer.timeout.connect(update)
            timer.start(slf.upate_every)
            
            ## Start Qt event loop unless running in interactive mode or using pyside.
             
            import sys
            if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
                QtGui.QApplication.instance().exec_()

        t = threading.Thread(target=runthr)
        t.daemon = True
        t.start()
