#! /usr/bin/python
# ---- Ed's notes --------
# event3.py
# draws mouse points & prints x,y
# see http://www.riverbankcomputing.com/pipermail/pyqt/2008-September/020562.html
# see http://harmattan-dev.nokia.com/docs/library/html/qt4/qpoint.html#details
# bigger example http://ftp.ics.uci.edu/pub/centos0/ics-custom-build/BUILD/PyQt-x11-gpl-4.7.2/examples/widgets/scribble.py
# event3.py
# ----- Changelog ---------
# - Originally created by Ed B on his laptop for the BBB challenge to control Pick N Place 
# - 2013-07-07: updated for Qt4 since Qt3 not available for BeagleBone Black on Debian 7.0, Ubuntu 13 or Angstrom [Drew (pdp7) & Bonnie (misterbonnie)

from PyQt4.Qt import *
from PyQt4 import QtGui, QtCore

import sys

# check out this QT serial library http://qt-project.org/wiki/QtSerialPort
# in leiu of serial port, redirect stdout  to file, then send file with comms program:
#  ~$ python ./event3.py >gcd.gcd


# LogFileName = None             # "print" Does not work inside of Python's IDLE
LogFileName = "stdout"         # a clue.. ..sys.stdout.write() does not work either

LogFileName = "Log.txt"      # Works inside with IDLE


# print "LogFileName: %s" % ( LogFileName )
# print "LogFileName: %s" % ( LogFileName )

# set origin offset
print 'g92 x0 y0'

# feedrate speed
print 'f10000'

# drive motors to 0, 0
print 'g0 x0 y0'

#-------

def Log_String( String, InitFile=False ) :
    if(   LogFileName == None )     :  print String

    elif( LogFileName == "stdout" ) :  sys.stdout.write( String )

    else :
        LogFile = open( "Log.txt", 'w' if(InitFile) else 'a' )
        LogFile.write( String + '\n' )
        LogFile.close()


#---

class Painting(QWidget):

    def __init__(self, *args):
        super(Painting, self).__init__()
        imageSize = QtCore.QSize(500, 500)
        self.image = QtGui.QImage(imageSize, QtGui.QImage.Format_RGB32)
        self.lastPoint = QtCore.QPoint()
        self.currentPos = QPoint(0,0)
        self.image.fill(QtGui.qRgb(255, 255, 255))

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(event.rect(), self.image)

    def mouseMoveEvent(self, ev):
        endPoint = ev.pos()
        painter = QtGui.QPainter(self.image)
        painter.setPen(QtGui.QPen(QtGui.QColor(20, 20, 20), 1, QtCore.Qt.SolidLine))
        painter.drawLine(self.currentPos, endPoint)
        self.modified = True
        self.update()
        self.currentPos=QPoint(endPoint)
        vx=self.currentPos.x()
        vy=self.currentPos.y()
        print 'DEBUG> MOVE ' + 'G1','X'+str(vx),'Y'+str(vy)
        #bitBlt(self, 0, 0, self.buffer)


    def mousePressEvent(self, ev):
        self.currentPos=QPoint(ev.pos())
        vx=self.currentPos.x()
        vy=self.currentPos.y()
        print 'DEBUG> PRESS' + 'G1','X'+str(vx),'Y'+str(vy)
        #bitBlt(self, 0, 0, self.buffer)

    #def resizeEvent(self, ev):
        #tmp = QPixmap(self.buffer.size())
        #bitBlt(tmp, 0, 0, self.buffer)
        #self.buffer.resize(ev.size())
        #self.buffer.fill()
        #bitBlt(self.buffer, 0, 0, tmp)

class MainWindow(QMainWindow):

    def __init__(self, *args):
        apply(QMainWindow.__init__, (self,) + args)
        self.painting=Painting(self)
        self.setCentralWidget(self.painting)

def main(args):
  app=QApplication(args)
  win=MainWindow()
  win.setGeometry(0, 0, 320, 280)
  win.setWindowTitle('Pick N Place')
  win.show()
  app.connect(app, SIGNAL("lastWindowClosed()")
                 , app
                 , SLOT("quit()")
                 )
  app.exec_()

if __name__=="__main__":
  main(sys.argv)
